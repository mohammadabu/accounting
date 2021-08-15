# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class CustomPrivacyVisibility(models.Model):

    _inherit = 'crm.lead'

    privacy_visibility = fields.Selection(selection_add=[('department', 'Department')])

    department = fields.Many2one('hr.department')
 


 