from odoo import fields, models , api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    check_hr_manager = fields.Selection(
        [
            ('yes', 'yes'),
            ('no','no')
        ]
        ,compute='_compute_hr_manager'
    ) 

    @api.depends()
    def _compute_hr_manager(self):
        uid = self.env.user.id
        user = self.env['res.users'].sudo().search([('id', '=', uid)], limit=1)
        if user.has_group('hr.group_hr_manager'):
            return 'yes'
        else:
            return 'no'