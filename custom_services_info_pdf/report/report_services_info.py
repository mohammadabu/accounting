# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ReportServicesInfo(models.AbstractModel):
    _name = 'report.custom_services_info_pdf.report_services_info'

    def get_services_info(self, docs):
        rec = ''
        if len(docs.stages) > 0 :
            arr = []
            for stage in docs.stages:
                arr.append(stage.id)    
            rec = self.env['services.services'].sudo().search([('active','=',1),('project_stage','in',arr)])
        else:
            rec = self.env['services.services'].sudo().search([('active','=',1)])
               

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
        docs = self.env['services_info.wizard'].sudo().browse(self.env.context.get('active_id'))
        services_info = self.get_services_info(docs)
        return {
            'doc_ids': self.ids,
            'docs': docs,
            'services_info': services_info[0],
        }