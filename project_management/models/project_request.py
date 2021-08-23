

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)



class ProjectRequest(models.Model):
    
    _name = 'project.request'
    _description = 'Project Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name                = fields.Char(string="Project Name",required=True,track_visibility=1)
    owner_name          = fields.Many2one('hr.employee',string='Owner Project Name',required=True,track_visibility=1)
    owner_dept          = fields.Many2one('hr.employee',string='Owner Dept.',required=True,track_visibility=1)
    expected_start      = fields.Date(string="Expected start date",required=True,track_visibility=1)
    expected_end        = fields.Date(string="Expected end date",required=True,track_visibility=1)
    estimated_budget    = fields.Float(string="Estimated budget",required=True,track_visibility=1)
    project_type        = fields.Selection([('internal', 'Internal'),('external', 'External')],required=True,track_visibility=1)
    project_description = fields.Html()  
    request_date        = fields.Date(compute='_compute_request_date')
    @api.depends()
    def _compute_request_date(self):
        self.request_date = datetime.today()


    justifications = fields.One2many('project.request.justification','request_id',ondelete='cascade') 

class ProjectRequestJustification(models.Model):

    _name = 'project.request.justification' 

    name  = fields.Char(string="Justifications")
    request_id = fields.Many2one('project.request') 