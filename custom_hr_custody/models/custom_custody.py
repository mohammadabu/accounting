# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class HrCustomCustody(models.Model):

    _name = 'hr.custody'
    _description = 'Hr Custody'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=True, readonly=True , states={'draft': [('readonly', False)]})
    employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]})
    employee = fields.Many2one('hr.employee',required=True, readonly=True,states={'draft': [('readonly', False)]})
    reason = fields.Char(required="1")
    notes = fields.Text()
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('approved', 'Approved'),
                              ('returned', 'Returned'), ('rejected', 'Refused')], string='Status', default='draft',
                             track_visibility='always')

    custody_lines = fields.One2many('hr.custody.lines', 'custody_id')      

    rejected_reason = fields.Text(string='Rejected Reason', copy=False, readonly=1, help="Reason for the rejection")                   

    def sent(self):
        self.state = 'to_approve'                         

    def approve(self):
        self.state = 'approved'    

class HrCustomCustodyLines(models.Model):

    _name = 'hr.custody.lines' 
    _sql_constraints = [('custody_item', 'unique (custody_id,custody_item)',     
                 'Duplicate Items in Custody line not allowed !')]
       
    custody_item = fields.Many2one('hr.custody.items',string="Items") 
    custody_qty = fields.Integer(string="Quantity")
    custody_id = fields.Many2one('hr.custody',string="Custody Id") 
    