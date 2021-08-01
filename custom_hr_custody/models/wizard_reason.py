# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class WizardReason(models.TransientModel):
    _name = 'wizard.reason'

    def send_reason(self):
        context = self._context
        reject_obj = self.env[context.get('model_id')].search([('id', '=', context.get('reject_id'))])
        reject_obj.write({'state': 'rejected',
                                'rejected_reason': self.reason})

    reason = fields.Text(string="Reason", help="Reason")
