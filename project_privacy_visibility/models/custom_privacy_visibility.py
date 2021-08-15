# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class CustomPrivacyVisibility(models.Model):

    _inherit = 'project.project'

    privacy_visibility = fields.Selection(selection_add=[('department', 'Department')])

    department = fields.Many2one('hr.department')

    user_emails = fields.Text()

    hide_product_id = fields.Selection(
        [
            ('yes', 'yes'),
            ('no','no')
        ]
        ,compute='_compute_hide_product_id'
    )
    @api.depends('department')
    def _compute_hide_product_id(self):
        arr_dep = []
        for dep in self.department:
            arr_dep.append(dep.id)
        employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id),('department_id','in',arr_dep)])
        if len(employee) > 0 :
            self.hide_product_id = 'no'
        else:
            self.hide_product_id = 'yes'    
        # if self.employee_id.parent_id != False:
        #     if self.employee_id.parent_id.user_id.id == self.env.user.id:
        #         self.hide_product_id = 'no'
        #     else:
        #         self.hide_product_id = 'yes'
        # else:
        #     self.hide_product_id = 'yes' 
    



 
