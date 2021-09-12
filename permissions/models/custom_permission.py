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
                            ('rejected', 'Refused')],
                            string='Status', default='draft',track_visibility='always',readonly=True)
     
    # date = fields.Date(required=True)
    # hour_from = fields.Selection([
    #     ('00:00', '12:00 AM'), ('00:30', '0:30 AM'),
    #     ('01:00', '1:00 AM'), ('01:30', '1:30 AM'),
    #     ('02:00', '2:00 AM'), ('02:30', '2:30 AM'),
    #     ('03:00', '3:00 AM'), ('03:30', '3:30 AM'),
    #     ('04:00', '4:00 AM'), ('04:30', '4:30 AM'),
    #     ('05:00', '5:00 AM'), ('05:30', '5:30 AM'),
    #     ('06:00', '6:00 AM'), ('06:30', '6:30 AM'),
    #     ('07:00', '7:00 AM'), ('07:30', '7:30 AM'),
    #     ('08:00', '8:00 AM'), ('08:30', '8:30 AM'),
    #     ('09:00', '9:00 AM'), ('09:30', '9:30 AM'),
    #     ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
    #     ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
    #     ('12:00', '12:00 PM'), ('12:30', '0:30 PM'),
    #     ('13:00', '1:00 PM'), ('13:30', '1:30 PM'),
    #     ('14:00', '2:00 PM'), ('14:30', '2:30 PM'),
    #     ('15:00', '3:00 PM'), ('15:30', '3:30 PM'),
    #     ('16:00', '4:00 PM'), ('16:30', '4:30 PM'),
    #     ('17:00', '5:00 PM'), ('17:30', '5:30 PM'),
    #     ('18:00', '6:00 PM'), ('18:30', '6:30 PM'),
    #     ('19:00', '7:00 PM'), ('19:30', '7:30 PM'),
    #     ('20:00', '8:00 PM'), ('20:30', '8:30 PM'),
    #     ('21:00', '9:00 PM'), ('21:30', '9:30 PM'),
    #     ('22:00', '10:00 PM'), ('22:30', '10:30 PM'),
    #     ('23:00', '11:00 PM'), ('23:30', '11:30 PM')], string='Hour from',required=True)
    # hour_to = fields.Selection([
    #     ('00:00', '12:00 AM'), ('00:30', '0:30 AM'),
    #     ('01:00', '1:00 AM'), ('01:30', '1:30 AM'),
    #     ('02:00', '2:00 AM'), ('02:30', '2:30 AM'),
    #     ('03:00', '3:00 AM'), ('03:30', '3:30 AM'),
    #     ('04:00', '4:00 AM'), ('04:30', '4:30 AM'),
    #     ('05:00', '5:00 AM'), ('05:30', '5:30 AM'),
    #     ('06:00', '6:00 AM'), ('06:30', '6:30 AM'),
    #     ('07:00', '7:00 AM'), ('07:30', '7:30 AM'),
    #     ('08:00', '8:00 AM'), ('08:30', '8:30 AM'),
    #     ('09:00', '9:00 AM'), ('09:30', '9:30 AM'),
    #     ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
    #     ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
    #     ('12:00', '12:00 PM'), ('12:30', '0:30 PM'),
    #     ('13:00', '1:00 PM'), ('13:30', '1:30 PM'),
    #     ('14:00', '2:00 PM'), ('14:30', '2:30 PM'),
    #     ('15:00', '3:00 PM'), ('15:30', '3:30 PM'),
    #     ('16:00', '4:00 PM'), ('16:30', '4:30 PM'),
    #     ('17:00', '5:00 PM'), ('17:30', '5:30 PM'),
    #     ('18:00', '6:00 PM'), ('18:30', '6:30 PM'),
    #     ('19:00', '7:00 PM'), ('19:30', '7:30 PM'),
    #     ('20:00', '8:00 PM'), ('20:30', '8:30 PM'),
    #     ('21:00', '9:00 PM'), ('21:30', '9:30 PM'),
    #     ('22:00', '10:00 PM'), ('22:30', '10:30 PM'),
    #     ('23:00', '11:00 PM'), ('23:30', '11:30 PM')], string='Hour to',required=True)

    from_date  = fields.Datetime(required=True)  
    to_date  = fields.Datetime(required=True)    
    
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
        check_in_date = str(self.from_date)
        check_out_date = str(self.to_date)
        _logger.info(check_in_date)
        _logger.info(check_out_date)
        attendance_vals = {
            'employee_id':self.employee.id, 
            'check_in': check_in_date,
            'check_out': check_out_date,
            'reason_modification': self.permission_type.id,
        }
        _logger.info(attendance_vals)
        attendance_id = self.env['hr.attendance'].sudo().create(attendance_vals)
        self.attendance_id = attendance_id.id        
    def refuse(self):
        self.state = 'rejected'
    def set_to_draft(self):
        self.state = 'draft'    



