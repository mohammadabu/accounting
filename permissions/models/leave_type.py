from odoo import fields, models


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    internal_assignment = fields.Char()