# -*- coding: utf-8 -*-

from odoo import models, fields


class OutsourcingInfo(models.TransientModel):
    _name = 'outsourcing_info.wizard'

    stages = fields.Many2many('outsourcing.outsourcing.stages')
    def print_outsourcing_info(self):
        data = {
            'stages': self.stages,
        }
        return self.env.ref('custom_outsourcing_info_pdf.action_report_print_outsourcing_info').report_action(self, data=data)

