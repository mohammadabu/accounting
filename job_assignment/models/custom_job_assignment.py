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

    name = fields.Char(required=True, readonly=True)
    employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]},default=_getDefaultEmployee)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('approved', 'Approved'),
                            ('rejected', 'Refused')], string='Status', default='draft',
                            track_visibility='always')

    
