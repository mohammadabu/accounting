# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class CustomHrEmployee(models.Model):

    _inherit = 'hr.employee'

    def write(self,values): 
        befory_edit_department = self.department_id.id
        before_edit_parent_id = self.parent_id.id
        before_edit_user_id = self.user_id.id
        rtn = super(CustomHrEmployee,self).write(values)
        after_edit_department = self.department_id.id
        after_edit_parent_id = self.parent_id.id
        after_edit_user_id = self.user_id.id
        # update department
        if befory_edit_department != after_edit_department or before_edit_user_id != after_edit_user_id:  
            self.pool.get("hr.employee").updateDepartmentEmails(self,befory_edit_department,after_edit_department)

        # update parent
        if before_edit_parent_id != after_edit_parent_id:
            self.pool.get("hr.employee").updateParentEmails(self,before_edit_parent_id,after_edit_parent_id)
        return rtn     

    @api.model
    def create(self,vals):
        try:   
            department = ''
            parent_id = ''
            user_id = ''
            if "department_id" in vals:
                department = vals['department_id']
            if "parent_id" in vals:
                parent_id = vals['parent_id']
            
            if "user_id" in vals:
                user_id = vals['user_id']
            # update department
            if department != False and department != "" and user_id != False and user_id != "":
                self.pool.get("hr.employee").updateDepartmentEmails(self,False,department)

            # update parent
            if parent_id != False and parent_id != "":
                self.pool.get("hr.employee").updateParentEmails(self,False,parent_id)    
        except:
            print("An exception occurred")                                  
        rtn = super(CustomHrEmployee,self).create(vals)
        return rtn 


    def updateDepartmentEmails(self,befory_edit_department,after_edit_department):
        employee_id = self.id
        employee_info = self.env['hr.employee'].sudo().search([('id','=',employee_id)],limit=1)
        user_id = ''
        if employee_info.user_id != False:
            user_id = employee_info.user_id.id
            user_id_string = "#" + str(user_id)+ "#"
            if befory_edit_department != False:
                project_before = self.env['project.project'].sudo().search([('user_emails','like',user_id_string),('department','=',befory_edit_department)])
                for project in project_before:
                    user_email = project.user_emails
                    user_email = user_email.replace(user_id_string,"") 
                    project.user_emails =  user_email

            project_after = self.env['project.project'].sudo().search([('department','=',after_edit_department)])
            for project_af in project_after:
                user_email = project_af.user_emails
                if user_email != False:
                    if user_id_string not in user_email:
                        user_email = user_email + "," + user_id_string
                else:
                    user_email = user_id_string
                project_af.user_emails =  user_email            

    def updateParentEmails(self,before_edit_parent_id,after_edit_parent_id):
        _logger.info("111")
