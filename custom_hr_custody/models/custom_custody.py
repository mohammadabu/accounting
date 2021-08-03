# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _


class HrCustomCustody(models.Model):

    _name = 'hr.custody'
    _description = 'Hr Custody'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _getDefaultEmployee(self):
        user_id = self.env.user.id
        employee = self.env['hr.employee'].sudo().search([('user_id','=',user_id)],limit=1)
        if len(employee) > 0 :
            return employee.id
        else:
            return False    
    name = fields.Char(required=True, readonly=True , states={'draft': [('readonly', False)]})
    employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]},default=_getDefaultEmployee)
    reason = fields.Char(required="1")
    notes = fields.Text()
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('approved', 'Approved'),
                            ('rejected', 'Refused')], string='Status', default='draft',
                            track_visibility='always')

    custody_lines = fields.One2many('hr.custody.lines', 'custody_id')      

    rejected_reason = fields.Text(string='Rejected Reason', copy=False, readonly=1, help="Reason for the rejection")                   

    def sent(self):
        self.state = 'to_approve'                         

    def approve(self):
        self.state = 'approved'    

    def set_to_draft(self):
        self.state = 'draft'    

    @api.model
    def create(self,vals):
        rtn = super(HrCustomCustody,self).create(vals)
        try:     
            custody_lines = self.custody_lines 
            _logger.info('create create create')
            _logger.info(custody_lines)
            # for line in custody_lines:
            #     _logger.info(line.custody_item)   
            #     _logger.info(line.custody_qty)    
            # _logger.info('create create create')    
            # custody_used = rtn.custody_used
            # amount_remaining = rtn.amount_remaining
            # raise exceptions.ValidationError("test")
        except Exception as e:
            raise exceptions.ValidationError(e)
            # raise exceptions.ValidationError(_('A problem has occurred, please check with the HR Department'))
         



class HrCustomCustodyLines(models.Model):

    _name = 'hr.custody.lines' 
    _sql_constraints = [('custody_item', 'unique (custody_id,custody_item)',     
                 'Duplicate Items in Custody line not allowed !')]

    custody_item = fields.Many2one('hr.custody.items',string="Items") 
    custody_qty = fields.Integer(string="Quantity")
    custody_id = fields.Many2one('hr.custody',string="Custody Id") 
    