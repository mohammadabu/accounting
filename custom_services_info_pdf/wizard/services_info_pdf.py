# -*- coding: utf-8 -*-

from odoo import models, fields


class ServicesInfo(models.TransientModel):
    _name = 'services_info.wizard'

    stages = fields.Many2many('services.services.stages')
    def print_services_info(self):
        data = {
            'stages': self.stages,
        }
        return self.env.ref('custom_services_info_pdf.action_report_print_services_info').report_action(self, data=data)

