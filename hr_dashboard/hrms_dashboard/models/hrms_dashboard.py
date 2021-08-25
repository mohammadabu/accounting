# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
from pytz import utc
from odoo import models, fields, api, _
from odoo.http import request
from odoo.tools import float_utils

ROUNDING_FACTOR = 16 


class HrLeave(models.Model):
    _inherit = 'hr.leave'
    duration_display = fields.Char('Requested (Days/Hours)', compute='_compute_duration_display', store=True,
                                   help="Field allowing to see the leave request duration"
                                        " in days or hours depending on the leave_type_request_unit")


class Employee(models.Model):
    _inherit = 'hr.employee'

    birthday = fields.Date('Date of Birth', groups="base.group_user", help="Birthday")

    @api.model
    def check_user_group(self):
        uid = request.session.uid
        user = self.env['res.users'].sudo().search([('id', '=', uid)], limit=1)
        if user.has_group('hr.group_hr_manager'):
            return True
        else:
            return False

    @api.model
    def get_user_employee_details(self):
        uid = request.session.uid
        employee = self.env['hr.employee'].sudo().search_read([('user_id', '=', uid)], limit=1)
        leaves_to_approve = self.env['hr.leave'].sudo().search_count([('state', 'in', ['confirm', 'validate1'])])
        today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        query = """
        select count(id)
        from hr_leave
        WHERE (hr_leave.date_from::DATE,hr_leave.date_to::DATE) OVERLAPS ('%s', '%s') and 
        state='validate'""" % (today, today)
        cr = self._cr
        cr.execute(query)
        leaves_today = cr.fetchall()
        first_day = date.today().replace(day=1)
        last_day = (date.today() + relativedelta(months=1, day=1)) - timedelta(1)
        query = """
                select count(id)
                from hr_leave
                WHERE (hr_leave.date_from::DATE,hr_leave.date_to::DATE) OVERLAPS ('%s', '%s')
                and  state='validate'""" % (first_day, last_day)
        cr = self._cr
        cr.execute(query)
        leaves_this_month = cr.fetchall()
        leaves_alloc_req = self.env['hr.leave.allocation'].sudo().search_count(
            [('state', 'in', ['confirm', 'validate1'])])
        timesheet_count = self.env['account.analytic.line'].sudo().search_count(
            [('project_id', '!=', False), ('user_id', '=', uid)])
        timesheet_view_id = self.env.ref('hr_timesheet.hr_timesheet_line_search')
        job_applications = self.env['hr.applicant'].sudo().search_count([])
        if employee:
            sql = """select broad_factor from hr_employee_broad_factor where id =%s"""
            self.env.cr.execute(sql, (employee[0]['id'],))
            result = self.env.cr.dictfetchall()
            broad_factor = result[0]['broad_factor']
            if employee[0]['birthday']:
                diff = relativedelta(datetime.today(), employee[0]['birthday'])
                age = diff.years
            else:
                age = False
            if employee[0]['joining_date']:
                diff = relativedelta(datetime.today(), employee[0]['joining_date'])
                years = diff.years
                months = diff.months
                days = diff.days
                experience = '{} years {} months {} days'.format(years, months, days)
            else:
                experience = False

            if employee[0]['department_id']:
                department = employee[0]['department_id']['name']
            else:
                department = False  

            if employee:
                data = {
                    'broad_factor': broad_factor if broad_factor else 0,
                    'leaves_to_approve': leaves_to_approve,
                    'leaves_today': leaves_today,
                    'leaves_this_month': leaves_this_month,
                    'leaves_alloc_req': leaves_alloc_req,
                    'emp_timesheets': timesheet_count,
                    'job_applications': job_applications,
                    'timesheet_view_id': timesheet_view_id,
                    'experience': experience,
                    'age': age,
                    'department':department
                }
                employee[0].update(data)
            return employee
        else:
            return False

    @api.model
    def get_dept_employee(self):
        cr = self._cr
        cr.execute("""select department_id, hr_department.name,count(*) 
            from hr_employee join hr_department on hr_department.id=hr_employee.department_id 
            group by hr_employee.department_id,hr_department.name""")
        dat = cr.fetchall()
        data = []
        for i in range(0, len(dat)):
            data.append({'label': dat[i][1], 'value': dat[i][2]})
        return data

    @api.model
    def get_department_leave(self):
        month_list = []
        graph_result = []
        for i in range(5, -1, -1):
            last_month = datetime.now() - relativedelta(months=i)
            text = format(last_month, '%B %Y')
            month_list.append(text)
        self.env.cr.execute("""select id, name from hr_department where active=True """)
        departments = self.env.cr.dictfetchall()
        department_list = [x['name'] for x in departments]
        for month in month_list:
            leave = {}
            for dept in departments:
                leave[dept['name']] = 0
            vals = {
                'l_month': month,
                'leave': leave
            }
            graph_result.append(vals)
        sql = """
        SELECT h.id, h.employee_id,h.department_id
             , extract('month' FROM y)::int AS leave_month
             , to_char(y, 'Month YYYY') as month_year
             , GREATEST(y                    , h.date_from) AS date_from
             , LEAST   (y + interval '1 month', h.date_to)   AS date_to
        FROM  (select * from hr_leave where state = 'validate') h
             , generate_series(date_trunc('month', date_from::timestamp)
                             , date_trunc('month', date_to::timestamp)
                             , interval '1 month') y
        where date_trunc('month', GREATEST(y , h.date_from)) >= date_trunc('month', now()) - interval '6 month' and
        date_trunc('month', GREATEST(y , h.date_from)) <= date_trunc('month', now())
        and h.department_id is not null
        """
        self.env.cr.execute(sql)
        results = self.env.cr.dictfetchall()
        leave_lines = []
        for line in results:
            employee = self.browse(line['employee_id'])
            from_dt = fields.Datetime.from_string(line['date_from'])
            to_dt = fields.Datetime.from_string(line['date_to'])
            days = employee.get_work_days_dashboard(from_dt, to_dt)
            line['days'] = days
            vals = {
                'department': line['department_id'],
                'l_month': line['month_year'],
                'days': days
            }
            leave_lines.append(vals)
        if leave_lines:
            df = pd.DataFrame(leave_lines)
            rf = df.groupby(['l_month', 'department']).sum()
            result_lines = rf.to_dict('index')
            for month in month_list:
                for line in result_lines:
                    if month.replace(' ', '') == line[0].replace(' ', ''):
                        match = list(filter(lambda d: d['l_month'] in [month], graph_result))[0]['leave']
                        dept_name = self.env['hr.department'].browse(line[1]).name
                        if match:
                            match[dept_name] = result_lines[line]['days']
        for result in graph_result:
            result['l_month'] = result['l_month'].split(' ')[:1][0].strip()[:3] + " " + \
                                result['l_month'].split(' ')[1:2][0]
        return graph_result, department_list

    def get_work_days_dashboard(self, from_datetime, to_datetime, compute_leaves=False, calendar=None, domain=None):
        resource = self.resource_id
        calendar = calendar or self.resource_calendar_id

        if not from_datetime.tzinfo:
            from_datetime = from_datetime.replace(tzinfo=utc)
        if not to_datetime.tzinfo:
            to_datetime = to_datetime.replace(tzinfo=utc)
        from_full = from_datetime - timedelta(days=1)
        to_full = to_datetime + timedelta(days=1)
        intervals = calendar._attendance_intervals(from_full, to_full, resource)
        day_total = defaultdict(float)
        for start, stop, meta in intervals:
            day_total[start.date()] += (stop - start).total_seconds() / 3600
        if compute_leaves:
            intervals = calendar._work_intervals(from_datetime, to_datetime, resource, domain)
        else:
            intervals = calendar._attendance_intervals(from_datetime, to_datetime, resource)
        day_hours = defaultdict(float)
        for start, stop, meta in intervals:
            day_hours[start.date()] += (stop - start).total_seconds() / 3600
        days = sum(
            float_utils.round(ROUNDING_FACTOR * day_hours[day] / day_total[day]) / ROUNDING_FACTOR
            for day in day_hours
        )
        return days

    @api.model
    def employee_leave_trend(self):
        leave_lines = []
        month_list = []
        graph_result = []
        for i in range(5, -1, -1):
            last_month = datetime.now() - relativedelta(months=i)
            text = format(last_month, '%B %Y')
            month_list.append(text)
        uid = request.session.uid
        employee = self.env['hr.employee'].sudo().search_read([('user_id', '=', uid)], limit=1)
        for month in month_list:
            vals = {
                'l_month': month,
                'leave': 0
            }
            graph_result.append(vals)
        sql = """
                SELECT h.id, h.employee_id
                     , extract('month' FROM y)::int AS leave_month
                     , to_char(y, 'Month YYYY') as month_year
                     , GREATEST(y                    , h.date_from) AS date_from
                     , LEAST   (y + interval '1 month', h.date_to)   AS date_to
                FROM  (select * from hr_leave where state = 'validate') h
                     , generate_series(date_trunc('month', date_from::timestamp)
                                     , date_trunc('month', date_to::timestamp)
                                     , interval '1 month') y
                where date_trunc('month', GREATEST(y , h.date_from)) >= date_trunc('month', now()) - interval '6 month' and
                date_trunc('month', GREATEST(y , h.date_from)) <= date_trunc('month', now())
                and h.employee_id = %s
                """
        self.env.cr.execute(sql, (employee[0]['id'],))
        results = self.env.cr.dictfetchall()
        for line in results:
            employee = self.browse(line['employee_id'])
            from_dt = fields.Datetime.from_string(line['date_from'])
            to_dt = fields.Datetime.from_string(line['date_to'])
            days = employee.get_work_days_dashboard(from_dt, to_dt)
            line['days'] = days
            vals = {
                'l_month': line['month_year'],
                'days': days
            }
            leave_lines.append(vals)
        if leave_lines:
            df = pd.DataFrame(leave_lines)
            rf = df.groupby(['l_month']).sum()
            result_lines = rf.to_dict('index')
            for line in result_lines:
                match = list(filter(lambda d: d['l_month'].replace(' ', '') == line.replace(' ', ''), graph_result))
                if match:
                    match[0]['leave'] = result_lines[line]['days']
        for result in graph_result:
            result['l_month'] = result['l_month'].split(' ')[:1][0].strip()[:3] + " " + \
                                result['l_month'].split(' ')[1:2][0]
        return graph_result


class BroadFactor(models.Model):
    _inherit = 'hr.leave.type'

    emp_broad_factor = fields.Boolean(string="Broad Factor", help="If check it will display in broad factor type")
