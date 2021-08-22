
from odoo import api, models, fields, exceptions, _


class hrAttendanceReasonModification(models.Model):
    _name = 'hr.attendance.reason.modification'
    _description = "Reason for changing attendance"

    name = fields.Char(string="Reason")