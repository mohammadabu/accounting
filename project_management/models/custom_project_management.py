
from odoo import models, fields, api, _


class ProjectManagement(models.Model):
    
    _name = 'project.management'
    _description = 'Project Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']