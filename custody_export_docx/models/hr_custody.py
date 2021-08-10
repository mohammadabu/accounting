import time
from datetime import date, datetime,timedelta
from calendar import monthrange
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
import pytz
import json
import io
from odoo import api, fields, models, _
import logging
# from docx import Document
# from docx.shared import Inches
from odoo.tools import date_utils
# from hijri_converter import convert
_logger = logging.getLogger(__name__)
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class HrCustodyDocuments(models.Model):
    _inherit = 'hr.custody'

    custodian_receipt = fields.Char()

    def generate_custodian_receipt_form(self):
        return self.pool.get("hr.custody.export.docx.wizard").action_export_custody_docx_report(self)


class SalaryDefinitionExportDocxWizard(models.TransientModel):
    _name = 'hr.custody.export.docx.wizard'
    _description = 'Docx Export Wizard'

    @api.model
    def action_export_custody_docx_report(self):
        return self.env.ref('custody_export_docx.custodian_receipt_docx').report_action(self)    