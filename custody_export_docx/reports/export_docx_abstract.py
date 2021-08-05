# -*- coding: utf-8 -*-

from sys import platform
from subprocess import Popen
from docx2pdf import convert
from datetime import datetime, date
import os
import base64
import logging
from odoo import models, tools
# from odoo.addons.sale_export_docx.reports import template
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, RGBColor, Inches , Cm
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import docx
_logger = logging.getLogger(__name__)

try:
    from docxtpl import DocxTemplate
except ImportError:
    _logger.debug('Can not import DocxTemplate')


class ExportDocxAbstract(models.AbstractModel):
    _name = 'export.docx.abstract'
    _description = 'Export Docx Abstract Model'

    def _get_objs_for_report(self, docids, data):
        if docids:
            ids = docids
        elif data and 'context' in data:
            ids = data["context"].get('active_ids', [])
        else:
            ids = self.env.context.get('active_ids', [])
        return self.env[self.env.context.get('active_model')].browse(ids)

    def create_docx_report(self, docids, data):
        objs = self._get_objs_for_report(docids, data)
        return self.generate_docx_report( data, objs), 'docx'

    def generate_docx_report(self, data, objs):
        raise NotImplementedError()

    def get_report_name(self, objs):
        raise NotImplementedError()