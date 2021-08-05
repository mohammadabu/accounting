# -*- coding: utf-8 -*-

from num2words import num2words
from sys import platform
from subprocess import Popen
from docx2pdf import convert
from datetime import datetime, date
import os
import base64
import logging
from odoo import models, tools,_
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

class CustodianReceiptExportDocx(models.AbstractModel):
    _name = 'report.custody_export_docx.custodian_receipt_docx'
    _inherit = 'export.docx.abstract'
    _description = 'Custodian Receipt Export Docx'



    def generate_docx_report(self, data, objs):
        timestamp = str(int(datetime.timestamp(datetime.now())))
        path_docx = '/var/lib/odoo/.local/share/Odoo/'
        # employee_id = objs.id
        # employee_data = self.pool.get("report.custody_export_docx.job_definition_docx").generate_variables(self,employee_id)
        document = docx.Document()
        document.add_heading('hello world')
        record = [
            [1,'mohammad',200],
            [2,'emad',300],
            [3,'abusubhia',400],
        ] 
        menuTable = document.add_table(rows=1,cols=3)
        menuTable.style = 'Table Grid'
        hdr_cells = menuTable.rows[0].cells
        hdr_cells[0].text = 'ID'
        hdr_cells[1].text = 'Name'
        hdr_cells[2].text = 'Price'
        for ID, name, price in record:
            row_Cells = menuTable.add_row().cells
            self.pool.get("report.custody_export_docx.custodian_receipt_docx").set_cell_border(self,row_Cells[0])
            row_Cells[0].text = str(ID)
            row_Cells[1].text = name
            row_Cells[2].text = str(price)

        path_docx = path_docx + '/EmployeeDocx_' + timestamp + "_" + "2131232132131321321" + ".docx"
        document.save(path_docx)
        
        report_doxc_path = path_docx
        with open(report_doxc_path, mode='rb') as file:
            fileContent = file.read()

        try:
            os.remove(report_doxc_path)
        except Exception as e:
            _logger.warning(repr(e))

        return fileContent

    def generate_variables(self, employee_id):
        hr_department = self.env['hr.department'].sudo().search([('internal_id','=','HR and Administration')])
        employee_info = self.env['hr.employee'].sudo().search([('id','=',employee_id)])
        identification_id = employee_info.identification_id
        identification_id_ar = self.pool.get("report.custody_export_docx.job_definition_docx").convertNumEnToAr(self,identification_id)
        iqama_number = employee_info.iqama_number
        iqama_job_ar = employee_info.iqama_job_ar
        iqama_job_en = employee_info.iqama_job_en
        job_ar = employee_info.job_ar
        job_en = employee_info.job_en
        employee_name_ar = employee_info.employee_name_ar
        employee_name_en = employee_info.name
        employee_nationality = employee_info.country_id.code or ''
        join_date = employee_info.date_joining or '0000/00'
        hr_manager = ""
        if hr_department.manager_id != False:
            hr_manager = hr_department.manager_id.employee_name_ar
        if join_date != '0000/00' and join_date != False:
            join_date = str(join_date).split("-")
            join_date = join_date[0] + "/" + join_date[1]
        join_date_ar = self.pool.get("report.custody_export_docx.job_definition_docx").convertNumEnToAr(self,join_date)
        iqama_number_ar = False
        if iqama_number != False:  
            iqama_number_ar = self.pool.get("report.custody_export_docx.job_definition_docx").convertNumEnToAr(self,iqama_number)

        if iqama_number == False:
            iqama_number = ""

        if iqama_job_ar == False:
            iqama_job_ar = ""

        if iqama_job_en == False:
            iqama_job_en = ""

        if job_ar == False:
            job_ar = ""

        if job_en == False:
            job_en = ""    

        if employee_name_ar == False:
            employee_name_ar = ""  

        if employee_name_en == False:
            employee_name_en = ""      

        if identification_id != False:
            identification_id = ""

        employee_date_array = {}
        employee_date_array['iqama_number_ar'] = iqama_number_ar
        employee_date_array['iqama_number'] = iqama_number
        employee_date_array['iqama_job_ar'] = iqama_job_ar
        employee_date_array['iqama_job_en'] = iqama_job_en
        employee_date_array['job_ar'] = job_ar
        employee_date_array['job_en'] = job_en
        employee_date_array['employee_name_ar'] = employee_name_ar
        employee_date_array['employee_name_en'] = employee_name_en
        employee_date_array['employee_nationality'] = employee_nationality
        employee_date_array['join_date'] = join_date
        employee_date_array['join_date_ar'] = join_date_ar
        employee_date_array['hr_manager'] = hr_manager
        employee_date_array['identification_id'] = identification_id
        employee_date_array['identification_id_ar'] = identification_id_ar
        return employee_date_array            


    def get_report_name(self, objs):
        timestamp = str(int(datetime.timestamp(datetime.now())))
        report_name = f'{objs.sale_order_id.id}_{objs.report_template_id.id}_{timestamp}_report.docx'
        return report_name


    def convertNumEnToAr(self,num):
        num = num.replace("1", "١", 15)
        num = num.replace("2", "٢", 15)
        num = num.replace("3", "٣", 15)
        num = num.replace("4", "٤", 15)
        num = num.replace("5", "٥", 15)
        num = num.replace("6", "٦", 15)
        num = num.replace("7", "٧", 15)
        num = num.replace("8", "٨", 15)
        num = num.replace("9", "٩", 15)
        num = num.replace("0", "٠", 15)
        return num


    def set_cell_border(self ,cell: _Cell, **kwargs):
        """
        Set cell`s border
        Usage:

        set_cell_border(
            cell,
            top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
            bottom={"sz": 12, "color": "#00FF00", "val": "single"},
            start={"sz": 24, "val": "dashed", "shadow": "true"},
            end={"sz": 12, "val": "dashed"},
        )
        """
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()

        # check for tag existnace, if none found, then create one
        tcBorders = tcPr.first_child_found_in("w:tcBorders")
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tcPr.append(tcBorders)

        # list over all available tags
        for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
            edge_data = kwargs.get(edge)
            if edge_data:
                tag = 'w:{}'.format(edge)

                # check for tag existnace, if none found, then create one
                element = tcBorders.find(qn(tag))
                if element is None:
                    element = OxmlElement(tag)
                    tcBorders.append(element)

                # looks like order of attributes is important
                for key in ["sz", "val", "color", "space", "shadow"]:
                    if key in edge_data:
                        element.set(qn('w:{}'.format(key)), str(edge_data[key]))
