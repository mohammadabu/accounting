
from odoo import models, fields, api, _


class HrEmployeeCustody(models.Model):
    _inherit = 'hr.employee'


    @api.model
    def getAllEmployeeCustody(self):
        custody = self.env['hr.custody.lines'].sudo().search([])
        self.employee_custody = custody
        # if self.parent_opportunity.id != False:
        #     custody = self.env['hr.custody.lines'].sudo().search(['&','|',('default_access_emails','like','#'+str(self.env.uid)+'#'),'|',('stage_access_emails','like','#'+str(self.env.uid)+'#'),'|',('assigned_resources_access_emails','like','#'+str(self.env.uid)+'#'),('owner_ownerManager_emails','like','#'+str(self.env.uid)+'#'),('parent_opportunity','=',self.parent_opportunity.id),('id','!=',self.id)])
        #     self.employee_custody = custody
        # else:
        #      self.employee_custody = []   
    # related_project = fields.Many2many('project.project','related_project','name_seq',compute='getAllRelatedProject')

    employee_custody = fields.One2many('hr.custody.lines', 'custody_id',compute='getAllEmployeeCustody')