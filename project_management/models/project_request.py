

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)



class ProjectRequest(models.Model):
    
    _name = 'project.request'
    _description = 'Project Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _getDefaultEmployee(self):
        user_id = self.env.user.id
        employee = self.env['hr.employee'].sudo().search([('user_id','=',user_id)],limit=1)
        if len(employee) > 0 :
            return employee.id
        else:
            return False  

    name                = fields.Char(string="Project Name",required=True,track_visibility=1)
    owner_name          = fields.Many2one('hr.employee',string='Owner Project Name',required=True,default=_getDefaultEmployee,track_visibility=1)
    owner_dept          = fields.Many2one('hr.employee',string='Owner Dept.',required=True,track_visibility=1)
    expected_start      = fields.Date(string="Expected start date",required=True,track_visibility=1)
    expected_end        = fields.Date(string="Expected end date",required=True,track_visibility=1)
    estimated_budget    = fields.Float(string="Estimated budget",required=True,track_visibility=1)
    project_type        = fields.Selection([('internal', 'Internal'),('external', 'External')],required=True,track_visibility=1)
    project_description = fields.Html()  
    request_date        = fields.Date(readonly=True)
    justifications      = fields.One2many('project.request.justification','request_id',ondelete='cascade') 
    objectives          = fields.One2many('project.main.objectives','request_id',ondelete='cascade') 
    deliverables        = fields.One2many('project.main.deliverables','request_id',ondelete='cascade') 
    # user_department     = fields.Integer(compute='_compute_user_department')
    # user_department     = fields.Integer()
    # current_user        = fields.Many2one('res.users', default=lambda self : self.env.uid)
    
    # @api.depends('current_user')
    # def _compute_user_department(self):
    #     user_employee = self.env['hr.employee'].sudo().search([('user_id','=',self.current_user.id)],limit=1) 
    #     if len(user_employee) > 0:
    #         self.user_department = int(user_employee.department_id.id)
    #     else:
    #         self.user_department = 0 


    @api.model
    def create(self,vals):
        vals['request_date'] = datetime.today()
        rtn = super(ProjectRequest,self).create(vals)
        return rtn 


    def unlink(self):
        for current in self:
            current_id = current.id
            self.env['project.request.justification'].sudo().search([('request_id','=',current_id)]).unlink()
            self.env['project.main.objectives'].sudo().search([('request_id','=',current_id)]).unlink()
            self.env['project.main.deliverables'].sudo().search([('request_id','=',current_id)]).unlink()
        rtn = super(ProjectRequest, self).unlink()
        return rtn

class ProjectRequestJustification(models.Model):

    _name = 'project.request.justification' 

    name  = fields.Char(string="Justifications")
    request_id = fields.Many2one('project.request') 

class ProjectMainObjectives(models.Model):

    _name = 'project.main.objectives' 

    name  = fields.Char(string="Objectives")
    request_id = fields.Many2one('project.request')

class ProjectMainDeliverables(models.Model):

    _name = 'project.main.deliverables' 

    name  = fields.Char(string="Deliverables")
    request_id = fields.Many2one('project.request')         