# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class HrCustomJobAssignment(models.Model):

    _name = 'hr.job.assignment'
    _description = 'Hr Job Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _getDefaultEmployee(self):
        user_id = self.env.user.id
        employee = self.env['hr.employee'].sudo().search([('user_id','=',user_id)],limit=1)
        if len(employee) > 0 :
            return employee.id
        else:
            return False 

    name = fields.Char(required=True, readonly=True)
    employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]},default=_getDefaultEmployee)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('approved', 'Approved'),
                            ('rejected', 'Refused')], string='Status', default='draft',
                            track_visibility='always',readonly=True)

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    duration = fields.Char(readonly=True)
    time_request = fields.Datetime(string="Time of the request",default=datetime.now(),readonly=True)
    note = fields.Text()

    def sent(self):
        self.state = 'to_approve'                         

    def approve(self):
        self.state = 'approved'    

    def set_to_draft(self):
        self.state = 'draft'    



