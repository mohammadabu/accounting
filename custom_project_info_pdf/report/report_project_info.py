# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ReportProjectInfo(models.AbstractModel):
    _name = 'report.custom_project_info_pdf.report_project_pdf'

    def get_project_info(self, docs):

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

        rec = self.env['project.project'].search([])


        records = []
        for r in rec:
            vals = {'name_seq': r.name_seq,
                    'name': r.name,
                    'stage': r.project_stage.name,
                    'parent_opportunity	': r.parent_opportunity.name,
                    }
            records.append(vals)
        return [records]

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['project_info.wizard'].browse(self.env.context.get('active_id'))
        # identification = []
        # for i in self.env['hr.employee'].search([('user_id', '=', docs.employee[0].id)]):
        #     if i:
        #         identification.append({'id': i.id, 'name': i.name})
        project_info = self.get_project_info(docs)
        # company_name = self.env['res.company'].search([('name', '=', docs.employee[0].company_id.name)])
        # period = None
        # if docs.from_date and docs.to_date:
        #     period = "From " + str(docs.from_date) + " To " + str(docs.to_date)
        # elif docs.from_date:
        #     period = "From " + str(docs.from_date)
        # elif docs.from_date:
        #     period = " To " + str(docs.to_date)
        # if len(identification) > 1:
        #     return {
        #         'doc_ids': self.ids,
        #         # 'doc_model': self.model,
        #         'docs': docs,
        #         'timesheets': timesheets[0],
        #         'total': timesheets[1],
        #         'company': company_name,
        #         'identification': identification,
        #         'period': period,
        #     }
        # else:
        #     return {
        #         'doc_ids': self.ids,
        #         # 'doc_model': self.model,
        #         'docs': docs,
        #         'timesheets': timesheets[0],
        #         'total': timesheets[1],
        #         'identification': identification,
        #         'company': company_name,
        #         'period': period,
        #     }

        return {
            'doc_ids': self.ids,
            'docs': docs,
            'project_info': timesheets[0],
        }