# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ReportProjectInfo(models.AbstractModel):
    _name = 'report.custom_project_info_pdf.report_project_info'

    def get_project_info(self, docs):
        # rec = ''
        # if len(docs.stages) > 0 :
        #     rec = self.env['project.project'].sudo().search([('active','=',1),('project_stage','in',docs.stages)])
        # else:
        #     rec = self.env['project.project'].sudo().search([('active','=',1)])

        rec = self.env['project.project'].sudo().search([('active','=',1)])

        records = []
        for r in rec:
            vals = {
                    'name_seq': r.name_seq,
                    'name': r.name,
                    'stage': r.project_stage.name,
                    'parent_opportunity': r.parent_opportunity.name,
                }
            records.append(vals)
        return [records]

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['project_info.wizard'].sudo().browse(self.env.context.get('active_id'))
        project_info = self.get_project_info(docs)
        return {
            'doc_ids': self.ids,
            'docs': docs,
            'project_info': project_info[0],
        }