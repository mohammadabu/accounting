# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ReportOutsourcingInfo(models.AbstractModel):
    _name = 'report.custom_outsourcing_info_pdf.report_outsourcing_info'

    def get_outsourcing_info(self, docs):
        rec = ''
        if len(docs.stages) > 0 :
            arr = []
            for stage in docs.stages:
                arr.append(stage.id)    
            rec = self.env['outsourcing.outsourcing'].sudo().search([('active','=',1),('project_stage','in',arr)])
        else:
            rec = self.env['outsourcing.outsourcing'].sudo().search([('active','=',1)])
               

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
        docs = self.env['outsourcing_info.wizard'].sudo().browse(self.env.context.get('active_id'))
        outsourcing_info = self.get_outsourcing_info(docs)
        return {
            'doc_ids': self.ids,
            'docs': docs,
            'outsourcing_info': outsourcing_info[0],
        }