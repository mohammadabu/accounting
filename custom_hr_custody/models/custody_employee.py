
from odoo import models, fields, api, _


class HrEmployeeCustody(models.Model):
    _inherit = 'hr.employee'


    @api.model
    def getAllEmployeeCustody(self):
        employee_id = self.id
        custody = self.env['hr.custody.lines'].sudo().search([('custody_id.employee','=',employee_id),('custody_id.state','=','approved')])
        self.employee_custody = custody
    employee_custody = fields.One2many('hr.custody.lines', 'custody_id',compute='getAllEmployeeCustody')