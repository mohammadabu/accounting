
from odoo import models, fields, api, _


class HrEmployeeCustody(models.Model):
    _inherit = 'hr.employee'

    employee_custody = fields.One2many('hr.custody', 'employee')