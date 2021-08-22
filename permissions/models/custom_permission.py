# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class HrCustomPermissions(models.Model):

    _name = 'hr.permissions'
    _description = 'Hr Permissions'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _getDefaultEmployee(self):
        user_id = self.env.user.id
        employee = self.env['hr.employee'].sudo().search([('user_id','=',user_id)],limit=1)
        if len(employee) > 0 :
            return employee.id
        else:
            return False 
    
    name = fields.Char(required=True)
    employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]},default=_getDefaultEmployee)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('direct_manager', 'Direct Manager Approved'),
                            ('hr_manager', 'Hr Approved'),('rejected', 'Refused')],
                            string='Status', default='draft',track_visibility='always',readonly=True)
     
    date = fields.Date(required=True)
    hour_from = fields.Selection([
        ('0', '12:00 AM'), ('0.5', '0:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '0:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], string='Hour from',required=True)
    hour_to = fields.Selection([
        ('0', '12:00 AM'), ('0.5', '0:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '0:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], string='Hour to',required=True)
    
    time_request = fields.Datetime(string="Time of the request",compute='_compute_time_request')
    @api.depends()
    def _compute_time_request(self):
        self.time_request = datetime.today()
    
    note = fields.Text(required=True)
    attachments = fields.Binary()
    
    is_direct_manager = fields.Selection(
        [
            ('yes', 'yes'),
            ('no','no')
        ]
        ,compute='_compute_is_direct_manager'
    )

    mandate_city = fields.Char()

    attendance_id = fields.Many2one('hr.attendance')
    permission_type = fields.Many2one('hr.attendance.reason.modification',required=True)

    @api.depends('employee')
    def _compute_is_direct_manager(self):
        if self.employee.parent_id != False:
            if self.employee.parent_id.user_id.id == self.env.user.id:
                self.is_direct_manager = 'yes'
            else:
                self.is_direct_manager = 'no'
        else:
            self.is_direct_manager = 'no' 


    def sent(self):
        self.state = 'to_approve'     
    def approve_direct_manager(self):
        self.state = 'direct_manager'    
    def approve_hr_manager(self):
        self.state = 'hr_manager'
        attendance_vals = {
            'employee_id':self.employee.id, 
            'check_in': '',
            'check_out': '',
            'reason_modification': self.permission_type.id,
        }
        attendance_id = self.env['hr.attendance'].sudo().create(attendance_vals)
        self.attendance_id = attendance_id.id
    def refuse(self):
        self.state = 'rejected'
    def set_to_draft(self):
        self.state = 'draft'    



