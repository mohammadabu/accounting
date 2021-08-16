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

    user_emails_department = fields.Text()

    def checkUserEmail(self):  

        pos_test = self.env['hr.employee'].sudo().search([('job_id','child_of',[115])])         
        _logger.info("pos_test") 
        _logger.info(pos_test) 
        all_user_emails = False
        if self.privacy_visibility == "department":
            project_department = self.department.id
            # get all employee department
            employees = self.env['hr.employee'].sudo().search([('department_id','=',project_department)])
            for emp in employees:
                if emp.user_id != False:
                    user_email = self.env['res.users'].search([('id','=',emp.user_id.id)])
                    if user_email.login != False:
                        if all_user_emails != False:
                            if user_email.login not in all_user_emails:
                                all_user_emails = all_user_emails + "," + "#" + str(user_email.id) + "#"
                        else:
                            all_user_emails = "#" + str(user_email.id) + "#"

            if self.department.manager_id != False:
                manager_department = self.department.manager_id
                if manager_department.user_id != False:
                    # get manager of department
                    user_email_dep = self.env['res.users'].search([('id','=',manager_department.user_id.id)])
                    if user_email_dep.login != False:
                        if all_user_emails != False:
                            if user_email_dep.login not in all_user_emails:
                                all_user_emails =  all_user_emails + "," + "#" + str(user_email_dep.id) + "#"
                        else:
                            all_user_emails = "#" + str(user_email_dep.id) + "#" 

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
                                            all_user_emails = all_user_emails + "," + "#" + str(manager_department.parent_id.user_id.id) + "#"
                                    else:
                                        all_user_emails = "#" + str(manager_department.parent_id.user_id.id) + "#"
                                manager_department = manager_department.parent_id 
                                _logger.info(manager_department)   
                            count_final = count_final + 1                    
                        else:
                            break
        
            # check department domain

        
        
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



    def checkUserEmailCreate(self):            
        all_user_emails = False
        _logger.info(self.privacy_visibility)
        if self.privacy_visibility == "department":
            project_department = self.department.id
            # get all employee department
            employees = self.env['hr.employee'].sudo().search([('department_id','=',project_department)])
            for emp in employees:
                if emp.user_id != False:
                    user_email = self.env['res.users'].search([('id','=',emp.user_id.id)])
                    if user_email.login != False:
                        if all_user_emails != False:
                            if user_email.login not in all_user_emails:
                                all_user_emails = all_user_emails + "," + "#" + str(user_email.id) + "#"
                        else:
                            all_user_emails = "#" + str(user_email.id) + "#"

            if self.department.manager_id != False:
                manager_department = self.department.manager_id
                if manager_department.user_id != False:
                    # get manager of department
                    user_email_dep = self.env['res.users'].search([('id','=',manager_department.user_id.id)])
                    if user_email_dep.login != False:
                        if all_user_emails != False:
                            if user_email_dep.login not in all_user_emails:
                                all_user_emails = all_user_emails + "," + "#" + str(user_email_dep.id) + "#"
                        else:
                            all_user_emails = "#" + str(user_email_dep.id) + "#" 

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
                                            all_user_emails = all_user_emails + "," + "#" + str(manager_department.parent_id.user_id.id) + "#" 
                                    else:
                                        all_user_emails = "#" + str(manager_department.parent_id.user_id.id) + "#"
                                manager_department = manager_department.parent_id 
                                _logger.info(manager_department)   
                            count_final = count_final + 1                    
                        else:
                            break
        self.user_emails =  all_user_emails

    @api.model
    def create(self,vals):
        try:   
            privacy_visibility = ''
            department = ''
            if "privacy_visibility" in vals:
                privacy_visibility = vals['privacy_visibility']
            if "department" in vals:
                department = vals['department']
            if privacy_visibility == "department":
                all_user_emails = False
                if privacy_visibility == "department":
                    project_department = department
                    # get all employee department
                    employees = self.env['hr.employee'].sudo().search([('department_id','=',project_department)])
                    for emp in employees:
                        if emp.user_id != False:
                            user_email = self.env['res.users'].search([('id','=',emp.user_id.id)])
                            if user_email.login != False:
                                if all_user_emails != False:
                                    if user_email.login not in all_user_emails:
                                        all_user_emails = all_user_emails + "," + "#" + str(user_email.id) + "#"
                                else:
                                    all_user_emails = "#" + str(user_email.id) + "#"
                    _logger.info("department.manager_id")
                    department = self.env['hr.department'].sudo().search([('id','=',department)])
                    _logger.info(department)
                    _logger.info(department.manager_id)
                    if department.manager_id != False:
                        manager_department = department.manager_id
                        _logger.info(manager_department)
                        if manager_department.user_id != False:
                            _logger.info(manager_department.user_id)
                            # get manager of department
                            user_email_dep = self.env['res.users'].search([('id','=',manager_department.user_id.id)])
                            if user_email_dep.login != False:
                                if all_user_emails != False:
                                    if user_email_dep.login not in all_user_emails:
                                        all_user_emails = all_user_emails + "," + "#" + str(user_email_dep.id) + "#"
                                else:
                                    all_user_emails = "#" + str(user_email_dep.id) + "#"

                    # get all parent manager of department
                    manager_department = department.manager_id
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
                                            all_user_emails = all_user_emails + "," + "#" + str(manager_department.parent_id.user_id.id) + "#"
                                    else:
                                        all_user_emails = "#" + str(manager_department.parent_id.user_id.id) + "#"
                                manager_department = manager_department.parent_id 
                                _logger.info(manager_department)   
                            count_final = count_final + 1                    
                        else:
                            break                               

                vals['user_emails'] = all_user_emails
        except:
            print("An exception occurred")                                  
        rtn = super(CustomPrivacyVisibility,self).create(vals)
        return rtn 

 
