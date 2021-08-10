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
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
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
        font_headerTable = document.styles.add_style('font_headerTable', WD_STYLE_TYPE.CHARACTER)
        font_headerTable.font.rtl = True
        font_headerTable.font.size = Pt(16)
        font_headerTable.font.bold = True
        font_headerTable.font.name = 'Arial'

        font_headerTable_1 = document.styles.add_style('font_headerTable_1', WD_STYLE_TYPE.CHARACTER)
        font_headerTable_1.font.rtl = True
        font_headerTable_1.font.size = Pt(12)
        font_headerTable_1.font.bold = True
        font_headerTable_1.font.name = 'Arial' 

        font_headerTable_2 = document.styles.add_style('font_headerTable_2', WD_STYLE_TYPE.CHARACTER)
        font_headerTable_2.font.rtl = True
        font_headerTable_2.font.size = Pt(10)
        font_headerTable_2.font.name = 'Arial' 

        font_headerTable_3 = document.styles.add_style('font_headerTable_3', WD_STYLE_TYPE.CHARACTER)
        font_headerTable_3.font.rtl = True
        font_headerTable_3.font.size = Pt(10)
        font_headerTable_3.font.bold = True
        font_headerTable_3.font.name = 'Arial' 

        # start Header Table  
        headerTable = document.add_table(rows=2,cols=2)

        headerTable.direction = WD_TABLE_DIRECTION.RTL
        headerTable_a_1 = headerTable.cell(0, 0)
        headerTable_b_1 = headerTable.cell(0, 1) 
        headerTable_a_1.merge(headerTable_b_1) 

        headerTable_cells = headerTable.rows[0].cells
        headerTable_cells[0].text = 'نموذج استلام عهده'
        headerTable_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        paragraph_headerTable = headerTable_cells[0].paragraphs[0]
        run_headerTable = paragraph_headerTable.runs
        run_headerTable[0].style = font_headerTable
        paragraph_headerTable.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
    
        headerTable_cells_1 = headerTable.rows[1].cells

        headerTable_cells_1[0].text = "التاريخ : ١ / ١ / ٢٠٢١ م"
        paragraph_headerTable_1 = headerTable_cells_1[0].paragraphs[0]
        run_headerTable_1 = paragraph_headerTable_1.runs
        run_headerTable_1[0].style = font_headerTable_1
        paragraph_headerTable_1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        headerTable_cells_1[1].text = "التاريخ : ١/١/١٤٤٢ هـ"
        paragraph_headerTable_2 = headerTable_cells_1[1].paragraphs[0]
        run_headerTable_2 = paragraph_headerTable_2.runs
        run_headerTable_2[0].style = font_headerTable_1
        paragraph_headerTable_2.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        # End Header Table 

        menuTable = document.add_table(rows=2,cols=6)
        menuTable.direction = WD_TABLE_DIRECTION.RTL
        menuTable.autofit = False 
        menuTable.allow_autofit = False
        menuTable.alignment = WD_TABLE_ALIGNMENT.CENTER

        a = menuTable.cell(0, 0)
        b = menuTable.cell(0,5)
        A = a.merge(b)        
        menuTable.style = 'Table Grid'

        hdr_cells = menuTable.rows[0].cells

        hdr_cells[0].text = 'بيانات المستلم'
        hdr_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        shading_elm_2 = parse_xml(r'<w:shd {} w:fill="#e5e5e5"/>'.format(nsdecls('w')))
        hdr_cells[0]._tc.get_or_add_tcPr().append(shading_elm_2)

        paragraph_header = hdr_cells[0].paragraphs[0]
        run_header = paragraph_header.runs
        run_header[0].style = font_headerTable_1
        paragraph_header.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


        hdr_cells_item = menuTable.rows[1].cells

        hdr_cells_item[0].text = 'مدير قسم العناية بالعملاء وإدارة الحسابات'
        hdr_cells_item[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        paragraph_item_0 = hdr_cells_item[0].paragraphs[0]
        run_item_0 = paragraph_item_0.runs
        run_item_0[0].style = font_headerTable_2
        paragraph_item_0.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        hdr_cells_item[1].text = 'المسمى الوظيفي'

        hdr_cells_item[1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        shading_cells_item_1 = parse_xml(r'<w:shd {} w:fill="#e5e5e5"/>'.format(nsdecls('w')))
        hdr_cells_item[1]._tc.get_or_add_tcPr().append(shading_cells_item_1)
        paragraph_item_1 = hdr_cells_item[1].paragraphs[0]
        run_item_1 = paragraph_item_1.runs
        run_item_1[0].style = font_headerTable_3
        paragraph_item_1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER



        hdr_cells_item[2].text = 'الإدارة العامة / الادارة العامة للعمليات / إدارة العمليات / العناية بالعملاء وادارة الحسابات'
        hdr_cells_item[2].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        paragraph_item_2 = hdr_cells_item[2].paragraphs[0]
        run_item_2 = paragraph_item_2.runs
        run_item_2[0].style = font_headerTable_2
        paragraph_item_2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


        hdr_cells_item[3].text = 'الإدارة'
        hdr_cells_item[3].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        shading_cells_item_3 = parse_xml(r'<w:shd {} w:fill="#e5e5e5"/>'.format(nsdecls('w')))
        hdr_cells_item[3]._tc.get_or_add_tcPr().append(shading_cells_item_3)
        paragraph_item_3 = hdr_cells_item[3].paragraphs[0]
        run_item_3 = paragraph_item_3.runs
        run_item_3[0].style = font_headerTable_3
        paragraph_item_3.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


        hdr_cells_item[4].text = 'أسامة عبدالله أحمد الزهراني'
        hdr_cells_item[4].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        paragraph_item_4 = hdr_cells_item[4].paragraphs[0]
        run_item_4 = paragraph_item_4.runs
        run_item_4[0].style = font_headerTable_2
        paragraph_item_4.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


        hdr_cells_item[5].text = 'اسـم المـوظف'
        hdr_cells_item[5].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        shading_cells_item = parse_xml(r'<w:shd {} w:fill="#e5e5e5"/>'.format(nsdecls('w')))
        hdr_cells_item[5]._tc.get_or_add_tcPr().append(shading_cells_item)
        paragraph_item_5 = hdr_cells_item[5].paragraphs[0]
        run_item_5 = paragraph_item_5.runs
        run_item_5[0].style = font_headerTable_3
        paragraph_item_5.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


        for cell in menuTable.columns[0].cells:
            cell.width = Cm(4.8)
        for cell in menuTable.columns[1].cells:
            cell.width = Cm(2.7)
        for cell in menuTable.columns[2].cells:
            cell.width = Cm(4.1)        
        for cell in menuTable.columns[3].cells:
            cell.width = Cm(1.3)
        for cell in menuTable.columns[4].cells:
            cell.width = Cm(3.2)
        for cell in menuTable.columns[5].cells:
            cell.width = Cm(2.1)            


        count = 1
        for row in menuTable.rows:
            if count == 2: 
                row.height = Cm(1.7)  
            else:
                row.height = Cm(0.7)   
            count = count + 1      

        tbl = menuTable._tbl
        count = 1
        for cell in tbl.iter_tcs():
            tcPr = cell.tcPr
            tcBorders = OxmlElement('w:tcBorders')

            top = OxmlElement('w:top')
            top.set(qn('w:val'), 'double')

            if count != 1:
                bottom = OxmlElement('w:bottom')
                bottom.set(qn('w:val'), 'double')

            if count != 1 and count != 2:
                left = OxmlElement('w:left')
                left.set(qn('w:val'), 'single')
            else:
                left = OxmlElement('w:left')
                left.set(qn('w:val'), 'double')

            if count != 1 and count != 7:
                right = OxmlElement('w:right')
                right.set(qn('w:val'), 'single')
            else :
                right = OxmlElement('w:right')
                right.set(qn('w:val'), 'double')    

                

            tcBorders.append(top)
            tcBorders.append(left)
            if count != 1:
                tcBorders.append(bottom)
            tcBorders.append(right)
            tcPr.append(tcBorders)
            count = count + 1
            
             
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


