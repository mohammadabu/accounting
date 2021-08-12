# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class HrCustomMandate(models.Model):

    _name = 'hr.mandate'
    _description = 'Hr Mandate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _getDefaultEmployee(self):
        user_id = self.env.user.id
        employee = self.env['hr.employee'].sudo().search([('user_id','=',user_id)],limit=1)
        if len(employee) > 0 :
            return employee.id
        else:
            return False 
    
    name = fields.Char(required=True)
    employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]},default=_getDefaultEmployee)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('direct_manager', 'Direct Manager Approved'),
                            ('hr_manager', 'Hr Approved'),('rejected', 'Refused')],
                            string='Status', default='draft',track_visibility='always',readonly=True)

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    duration = fields.Char(compute="_compute_expected_duration")
    duration_int = fields.Char(compute="_compute_expected_duration")
    time_request = fields.Datetime(string="Time of the request",default=datetime.now(),readonly=True)
    note = fields.Text(required=True)
    attachments = fields.Binary()
    
    is_direct_manager = fields.Selection(
        [
            ('yes', 'yes'),
            ('no','no')
        ]
        ,compute='_compute_is_direct_manager'
    )

    mandate_city = fields.Char()

    leave_id = fields.Many2one('hr.leave')

    @api.depends('employee')
    def _compute_is_direct_manager(self):
        if self.employee.parent_id != False:
            if self.employee.parent_id.user_id.id == self.env.user.id:
                self.is_direct_manager = 'yes'
            else:
                self.is_direct_manager = 'no'
        else:
            self.is_direct_manager = 'no' 


    @api.onchange('date_from','date_to') 
    def _compute_expected_duration(self):
        for rec in self:
            from_date = rec.date_from
            to_date = rec.date_to
            if from_date != False and to_date != False:
                duration = to_date - from_date
                count = 0
                for i in range(duration.days + 1):
                    dayRange = from_date + timedelta(days=i)
                    dayRange_day = dayRange.strftime("%A")
                    if dayRange_day != "Friday" and dayRange_day != "Saturday":
                        count = count + 1
                duration = count
                rec.duration = str(duration) + " " + _("days")
                rec.duration_int = str(duration)
            else:
                rec.duration = "0 "+ _("days")
                rec.duration_int = 0


    def sent(self):
        self.state = 'to_approve'     
        if self.leave_id:
            self.leave_id.write({'state': 'confirm'})                    
    def approve_direct_manager(self):
        if self.leave_id:
            self.leave_id.write({'state': 'confirm'})
        self.state = 'direct_manager'    
    def approve_hr_manager(self):
        self.state = 'hr_manager'
        # Check If leave type exist
        check_leave_type = self.env['hr.leave.type'].sudo().search([('internal_mandate','=','mandate')])
        if len(check_leave_type) <= 0:
            leave_type_vals = {
                'internal_mandate':'mandate',
                'name': 'انتداب',
                'validation_type': 'no_validation',
                'type': 'paid_time_off',
                'allocation_type':'no',
                'color_name':'red',
                'request_unit':'day'
            }
            check_leave_type = self.env['hr.leave.type'].sudo().create(leave_type_vals)
        check_leave_type = check_leave_type.id
        if not self.leave_id:
            _logger.info("self.leave_id")
            leave_vals = {
                'employee_id':self.employee.id,
                'holiday_status_id': check_leave_type,
                'request_date_from': self.date_from,
                'request_date_to': self.date_to,
                'number_of_days': self.duration_int,
                'number_of_days_display': self.duration_int,
                'state':'validate'
            }
            leave = self.env['hr.leave'].sudo().create(leave_vals)
            self.leave_id = leave.id
        else:
            self.leave_id.write({'state': 'validate'})   
    def refuse(self):
        self.state = 'rejected'
        if self.leave_id:
            self.leave_id.write({'state': 'confirm'})
    def set_to_draft(self):
        if self.leave_id:
            self.leave_id.write({'state': 'confirm'})
        self.state = 'draft'    



