# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ReportProjectInfo(models.AbstractModel):
    _name = 'report.custom_project_info_pdf.report_project_pdf'

    def get_timesheets(self, docs):

        # if docs.from_date and docs.to_date:
        #     rec = self.env['account.analytic.line'].search([('user_id', '=', docs.employee[0].id),
        #                                                     ('date', '>=', docs.from_date),
        #                                                     ('date', '<=', docs.to_date)])
        # elif docs.from_date:
        #     rec = self.env['account.analytic.line'].search([('user_id', '=', docs.employee[0].id),
        #                                                     ('date', '>=', docs.from_date)])
        # elif docs.to_date:
        #     rec = self.env['account.analytic.line'].search([('user_id', '=', docs.employee[0].id),
        #                                                     ('date', '<=', docs.to_date)])
        # else:
        #     rec = self.env['account.analytic.line'].search([('user_id', '=', docs.employee[0].id)])

        rec = self.env['project.project'].search([('project.project', '=', docs.employee[0].id)])


        records = []
        total = 0
        for r in rec:
            vals = {'project': r.project_id.name,
                    'user': r.user_id.partner_id.name,
                    'duration': r.unit_amount,
                    'date': r.date,
                    }
            total += r.unit_amount
            records.append(vals)
        return [records, total]

    @api.model
    def _get_report_values(self, docids, data=None):
        """we are overwriting this function because we need to show values from other models in the report
        we pass the objects in the docargs dictionary"""
        docs = self.env['timesheet.wizard'].browse(self.env.context.get('active_id'))
        identification = []
        for i in self.env['hr.employee'].search([('user_id', '=', docs.employee[0].id)]):
            if i:
                identification.append({'id': i.id, 'name': i.name})
        timesheets = self.get_timesheets(docs)
        company_name = self.env['res.company'].search([('name', '=', docs.employee[0].company_id.name)])
        period = None
        if docs.from_date and docs.to_date:
            period = "From " + str(docs.from_date) + " To " + str(docs.to_date)
        elif docs.from_date:
            period = "From " + str(docs.from_date)
        elif docs.from_date:
            period = " To " + str(docs.to_date)
        if len(identification) > 1:
            return {
                'doc_ids': self.ids,
                # 'doc_model': self.model,
                'docs': docs,
                'timesheets': timesheets[0],
                'total': timesheets[1],
                'company': company_name,
                'identification': identification,
                'period': period,
            }
        else:
            return {
                'doc_ids': self.ids,
                # 'doc_model': self.model,
                'docs': docs,
                'timesheets': timesheets[0],
                'total': timesheets[1],
                'identification': identification,
                'company': company_name,
                'period': period,
            }
