# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class HrCustomCustody(models.Model):

    _name = 'hr.custody'
    _description = 'Hr Custody'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required="1")
    employee = fields.Many2one('hr.employee',required="1")
    reason = fields.Char(required="1")
    notes = fields.Text()
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('approved', 'Approved'),
                              ('returned', 'Returned'), ('rejected', 'Refused')], string='Status', default='draft',
                             track_visibility='always')

    def sent(self):
        self.state = 'to_approve'                         

    def approve(self):
        for custody in self.env['hr.custody'].search([('name', '=', self.name.id)]):
            if custody.state == "approved":
                raise UserError(_("Custody is not available now"))
        self.state = 'approved'    