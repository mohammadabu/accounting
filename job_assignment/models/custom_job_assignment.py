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
    # employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]},default=_getDefaultEmployee)
    # reason = fields.Char(required="1")
    # notes = fields.Text()
    # state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('approved', 'Approved'),
    #                         ('rejected', 'Refused')], string='Status', default='draft',
    #                         track_visibility='always')
    # custody_lines = fields.One2many('hr.custody.lines', 'custody_id',ondelete='cascade')      
    # rejected_reason = fields.Text(string='Rejected Reason', copy=False, readonly=1, help="Reason for the rejection")                   

    
