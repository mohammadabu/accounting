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
        all_user_emails = False
        if self.privacy_visibility == "department":
            project_department = self.department.id
            # get all employee department
            employees = self.env['hr.employee'].sudo().search([('department_id','=',project_department)])
            for emp in employees:
                if emp.user_id != False:
                    user_email = self.env['res.users'].search([('id','=',emp.user_id.id)])
                    # if user_email.login != False:
                    #     if all_user_emails != False:
                    #         if user_email.login not in all_user_emails:
                    #             all_user_emails = all_user_emails + "," + user_email.login
                    #     else:
                    #         all_user_emails = user_email.login

            if self.department.manager_id != False:
                manager_department = self.department.manager_id
                if manager_department.user_id != False:
                    # get manager of department
                    user_email_dep = self.env['res.users'].search([('id','=',manager_department.user_id.id)])
                    # if user_email_dep.login != False:
                    #     if all_user_emails != False:
                    #         if user_email_dep.login not in all_user_emails:
                    #             all_user_emails = all_user_emails + "," + user_email_dep.login
                    #     else:
                    #         all_user_emails = user_email_dep.login  

                    # get all parent manager of department

                    i = 0
                    count_final = 0
                    while i <= 10:
                        if count_final < 200:
                            _logger.info("start")
                            _logger.info(manager_department.parent_id)
                            _logger.info(manager_department.parent_id.name)
                            if len(manager_department.parent_id) > 0:
                                if manager_department.parent_id.user_id != False:
                                    if all_user_emails != False:
                                        if manager_department.parent_id.user_id.login not in all_user_emails:
                                            all_user_emails = all_user_emails + "," + manager_department.parent_id.user_id.login
                                    else:
                                        all_user_emails = manager_department.parent_id.user_id.login 
                                manager_department = manager_department.parent_id 
                                _logger.info(manager_department)   
                            count_final = count_final + 1                    
                        else:
                            break


        self.user_emails = all_user_emails
                




    def write(self,values):
        befory_edit_privacy_visibility = self.privacy_visibility
        before_edit_department = self.department.id
        rtn = super(CustomPrivacyVisibility,self).write(values)
        after_edit_privacy_visibility = self.privacy_visibility
        after_edit_department = self.department.id
        if befory_edit_privacy_visibility != after_edit_privacy_visibility or before_edit_department != after_edit_department:
            self.pool.get("project.project").checkUserEmail(self)
        return rtn     


 
