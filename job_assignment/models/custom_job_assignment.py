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
    
    name = fields.Char(required=True)
    employee = fields.Many2one('hr.employee',required=True, readonly=True ,states={'draft': [('readonly', False)]},default=_getDefaultEmployee)
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'Waiting For Approval'), ('direct_manager', 'Direct Manager Approved'),
                            ('hr_manager', 'Hr Approved'),('rejected', 'Refused')],
                            string='Status', default='draft',track_visibility='always',readonly=True)

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    duration = fields.Char(compute="_compute_expected_duration")
    time_request = fields.Datetime(string="Time of the request",default=datetime.now(),readonly=True)
    note = fields.Text(required=True)
    attachments = fields.Binary()
    
    is_direct_manager = fields.Selection(
        [
            ('yes', 'yes'),
            ('no','no')
        ]
        ,compute='_compute_is_direct_manager'
    )

    @api.depends('employee')
    def _compute_is_direct_manager(self):
        if self.employee.parent_id != False:
            if self.employee.parent_id.user_id.id == self.env.user.id:
                self.is_direct_manager = 'yes'
            else:
                self.is_direct_manager = 'no'
        else:
            self.is_direct_manager = 'no' 


    @api.onchange('date_from','date_to') 
    def _compute_expected_duration(self):
        for rec in self:
            from_date = rec.date_from
            to_date = rec.date_to
            if from_date != False and to_date != False:
                duration = to_date - from_date
                count = 0
                for i in range(duration.days + 1):
                    dayRange = from_date + timedelta(days=i)
                    dayRange_day = dayRange.strftime("%A")
                    if dayRange_day != "Friday" and dayRange_day != "Saturday":
                        count = count + 1
                duration = count
                rec.duration = str(duration) + " " + _("days")
            else:
                rec.duration = "0 "+ _("days")


    def sent(self):
        self.state = 'to_approve'                         
    def approve_direct_manager(self):
        self.state = 'direct_manager'    
    def approve_hr_manager(self):
        self.state = 'hr_manager'
    def refuse(self):
        self.state = 'rejected'
    def set_to_draft(self):
        self.state = 'draft'    



