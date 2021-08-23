
from odoo import models, fields, api, _


class ProjectRequest(models.Model):
    
    _name = 'project.request'
    _description = 'Project Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']