# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

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
            custody_lines = rtn.custody_lines 
            error = 0
            _logger.info("---------required_quantity------------")
            for line in custody_lines:
                custody_used_item = self.env['hr.custody.lines'].sudo().search([('custody_item','=',line.custody_item.id),('custody_id.state','=','approved')])                
                required_quantity = line.custody_item.required_quantity
                _logger.info(required_quantity)   
                _logger.info(custody_used_item)   
            _logger.info("---------required_quantity------------")  
        except Exception as e:
            raise exceptions.ValidationError(e)
            # raise exceptions.ValidationError(_('A problem has occurred, please check with the HR Department'))
        return rtn




class HrCustomCustodyLines(models.Model):

    _name = 'hr.custody.lines' 
    _sql_constraints = [('custody_item', 'unique (custody_id,custody_item)',     
                 'Duplicate Items in Custody line not allowed !')]

    custody_item = fields.Many2one('hr.custody.items',string="Items") 
    custody_qty = fields.Integer(string="Quantity")
    custody_id = fields.Many2one('hr.custody',string="Custody Id") 
    