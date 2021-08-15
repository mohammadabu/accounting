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


    def checkUserEmail(self):
        all_project = self.env['project.project'].sudo().search([])
        for project in all_project:
            all_user_emails = ''
            if project.privacy_visibility == "department":
                project_department = project.department.id
                # get all employee department
                employees = self.env['hr.employee'].sudo().search([('department_id','=',project_department)])
                for emp in employees:
                    if emp.user_id != False:
                        user_email = self.env['res.users'].search([('id','=',emp.user_id.id)])
                        if user_email.login != False:
                            if all_user_emails != False:
                                if user_email.login not in all_user_emails:
                                    all_user_emails = all_user_emails + "," + user_email.login
                            else:
                                all_user_emails = user_email.login
            project.user_emails = all_user_emails
                




    def write(self,values):
        befory_edit_privacy_visibility = self.privacy_visibility
        before_edit_department = self.department.id
        rtn = super(CustomPrivacyVisibility,self).write(values)
        after_edit_privacy_visibility = self.privacy_visibility
        after_edit_department = self.department.id
        _logger.info("sadsadasdsas12321312332121332213dasad")
        if befory_edit_privacy_visibility != after_edit_privacy_visibility or before_edit_department != after_edit_department:
            _logger.info("sadsadasdsasdasad")
            self.pool.get("project.project").checkUserEmail(self)
        return rtn     


 
