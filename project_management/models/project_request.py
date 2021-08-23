

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)



class ProjectRequest(models.Model):
    
    _name = 'project.request'
    _description = 'Project Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name                = fields.Char(string="Project Name",required=True)
    owner_name          = fields.Many2one('hr.employee',string='Owner Project Name',required=True)
    owner_dept          = fields.Many2one('hr.employee',string='Owner Dept.',required=True)
    expected_start      = fields.Date(string="Expected start date",required=True)
    expected_end        = fields.Date(string="Expected end date",required=True)
    estimated_budget    = fields.Float(string="Estimated budget",required=True)
    project_type        = fields.Selection([('internal', 'Internal'),('external', 'External')],required=True)
    project_description = fields.Html()  
    request_date        = fields.Date(compute='_compute_request_date')
    @api.depends()
    def _compute_request_date(self):
        self.request_date = datetime.today()