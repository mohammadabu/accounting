from odoo import api, models, fields, exceptions, _
import logging
import base64
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz
from xlrd import open_workbook
import tempfile
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):

    _inherit = 'hr.attendance'

    notes = fields.Char()
    def remove_finish_import_crons(self):
        master_partners = self.env['import.attendances.master'].search(
            ['|', ('status', '=', 'imported'), ('status', '=', 'failed')])
        # Remove completed crons
        for master_part in master_partners:
            if master_part.cron_id:
                master_part.cron_id.unlink()
        # Remove the Import status lines
        imported_master_part = self.env['import.attendances.master'].search(
            [('status', '=', 'imported')])
        imported_master_part.unlink()
    @api.model
    def convert24(self,str1):
        time_arr = {
            "00":12,
            "01":13,
            "02":14,
            "03":15,
            "04":16,
            "05":17,
            "06":18,
            "07":19,
            "08":20,
            "09":21,
            "10":22,
            "11":23,
            "12":00
        }
        check_in_time = str1[0]
        check_in_time = check_in_time.replace("\u200f","")
        check_in_time_split = check_in_time.split(":")
        hours = check_in_time_split[0]
        minutes = check_in_time_split[1]
        check_in_zone = str1[1]
        if check_in_zone == "ص" and hours == "12":
            return "00:"+minutes
        elif check_in_zone == "ص":
            return hours+":"+ minutes
        elif check_in_zone == "م" and hours == "12":
            return "12"+":"+ minutes
        else:
            
            # _logger.info(time_arr[hours])
            # _logger.info(minutes)
            return str(time_arr[hours]) + ":" + minutes          
    def import_data(self, part_master_id=False):
        if part_master_id:
            part_master = self.env[
                'import.attendances.master'].browse(part_master_id)
            total_success_import_record = 0
            total_failed_record = 0
            list_of_failed_record = ''
            datafile = part_master.file
            file_name = str(part_master.filename)
            attendance_obj = self.env['hr.attendance']
            state_obj = self.env['res.country.state']
            country_obj = self.env['res.country']
            try:
                if not datafile or not \
                        file_name.lower().endswith(('.xls', '.xlsx')):
                    list_of_failed_record += "Please Select an .xls file to Import."
                    _logger.error(
                        "Please Select an .xls file to Import.")
                if part_master.type == 'xlsx':
                    if not datafile or not file_name.lower().endswith(('.xls', '.xlsx',)):
                        list_of_failed_record += "Please Select an .xls or its compatible file to Import."
                        _logger.error(
                            "Please Select an .xls or its compatible file to Import.")
                    temp_path = tempfile.gettempdir()
                    file_data = base64.decodestring(datafile)
                    _logger.info("file_data")
                    _logger.info(file_data)
                    fp = open(temp_path + '/xsl_file.xls', 'wb+')
                    fp.write(file_data)
                    fp.close()
                    wb = open_workbook(temp_path + '/xsl_file.xls')
                    data_list = []
                    header_list = []
                    headers_dict = {}
                    for sheet in wb.sheets():
                        _logger.info(sheet.nrows)
                    #     # Sales data xlsx
                        first_row = 0
                        emp_name_row = 0
                        date_row = 0
                        check_in_row = 0
                        check_out_row = 0
                        for rownum in range(sheet.nrows):
                            # _logger.info(rownum)
                            # _logger.info(sheet.row_values(rownum))
                            item = sheet.row_values(rownum)
                            if "اسم الموظف" in item and "التاريخ" in item and "وقت دخول" in item and "وقت الخروج" in item:
                                first_row = rownum
                                for idx1,item1 in enumerate(item):
                                    if item1 == "اسم الموظف":
                                        emp_name_row = idx1
                                    if item1 == "التاريخ":
                                        date_row = idx1
                                    if item1 == "وقت دخول":
                                        check_in_row = idx1
                                    if item1 == "وقت الخروج":
                                        check_out_row = idx1
                                break    

                        for rownum1 in range(sheet.nrows): 
                            item_y = sheet.row_values(rownum1)           
                            if rownum1 > first_row:
                                emp_name =  item_y[emp_name_row]
                                date = item_y[date_row] 
                                check_in = item_y[check_in_row]     
                                check_out = item_y[check_out_row] 
                                full_date_check_in = False
                                full_date_check_out = False
                                if emp_name != "" and (check_in != "" or check_out != ""):  
                                    if check_in:
                                        split_check_in = check_in.split(" ")
                                        if len(split_check_in) > 1:
                                            try:
                                                date = date.replace("/","-",3)
                                                new_time = self.pool.get("hr.attendance").convert24(self,split_check_in)
                                                new_time = new_time.replace("\u200f","")
                                                full_date_time = date + " " + new_time + ":00"
                                                full_date_check_in = datetime.strptime(full_date_time, '%Y-%m-%d %H:%M:%S')
                                            except Exception as e:
                                                _logger.info("----error in------")   
                                                _logger.info(e) 
                                    if check_out:
                                        split_check_out = check_out.split(" ")
                                        if len(split_check_out) > 1:  
                                            try:
                                                date = date.replace("/","-",3)
                                                new_time = self.pool.get("hr.attendance").convert24(self,split_check_out)
                                                full_date_time = date + " " + new_time + ":00"
                                                full_date_check_out = datetime.strptime(full_date_time, '%Y-%m-%d %H:%M:%S')
                                            except Exception as e:
                                                _logger.info("----error out------")    
                                                _logger.info(e)   
                                # if  full_date_check_in != False or full_date_check_out != False:
                                if  full_date_check_in != False :
                                    try:
                                        emp_name_info = self.env['hr.employee'].sudo().search([('name','=',emp_name)])
                                        attendance_vals = {
                                            'employee_id': emp_name_info.id,
                                            'check_in': full_date_check_in,
                                            'check_out': full_date_check_out
                                        }
                                        self.env['hr.attendance'].sudo().create(attendance_vals)
                                        _logger.info(full_date_check_in)
                                        _logger.info(full_date_check_out)
                                        _logger.info(emp_name)
                                        _logger.info(emp_name_info)  
                                        total_success_import_record += 1  
                                    except Exception as e:
                                        total_failed_record += 1
                                        list_of_failed_record += "| Error at Line :" + str(rownum1 + 1) + " |"
                                        _logger.error("Error at %s" % str(rownum1))    
                                else:
                                    if emp_name != "":
                                        total_failed_record += 1
                                        list_of_failed_record += "| Error at Line :" + str(rownum1 + 1) + " |"
                                        _logger.error("Error at %s" % str(rownum1))                         
            except Exception as e:
                list_of_failed_record += str(e)
            _logger.info("list_of_failed_record")
            _logger.info(list_of_failed_record)


            try:
                file_data = base64.b64encode(
                    list_of_failed_record.encode('utf-8'))
                part_master.status = 'imported'
                datetime_object = datetime.strptime(
                    str(part_master.create_date), '%Y-%m-%d %H:%M:%S.%f')
                start_date = datetime.strftime(
                    datetime_object, DEFAULT_SERVER_DATETIME_FORMAT)
                self._cr.commit()
                now_time = datetime.now()
                user_tz = self.env.user.tz or str(pytz.utc)
                local = pytz.timezone(user_tz)
                start_date_in_user_tz = datetime.strftime(pytz.utc.localize(
                    datetime.strptime(str(start_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(
                    local), DEFAULT_SERVER_DATETIME_FORMAT)
                end_date_in_user_tz = datetime.strftime(pytz.utc.localize(
                    now_time).astimezone(local),
                    DEFAULT_SERVER_DATETIME_FORMAT)
                self.env['import.attendances.history'].create({
                    'total_success_count': total_success_import_record,
                    'total_failed_count': total_failed_record,
                    'file': file_data,
                    'file_name': 'report_importazione.txt',
                    'type': part_master.type,
                    'import_file_name': part_master.filename,
                    'start_date': start_date_in_user_tz,
                    'end_date': end_date_in_user_tz,
                    'operation': part_master.operation,
                })
                if part_master.user_id:
                    message = "Import process is completed. Check in Imported attendances History if all the attendances have" \
                              " been imported correctly. </br></br> Imported File: %s </br>" \
                              "Imported by: %s" % (
                                  part_master.filename, part_master.user_id.name)
                    part_master.user_id.notify_partner_info(
                        message, part_master.user_id, sticky=True)
                self._cr.commit()
            except Exception as e:
                part_master.status = 'failed'
                _logger.error(e)
                self._cr.commit()
