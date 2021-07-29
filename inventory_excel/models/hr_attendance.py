from odoo import api, models, fields, exceptions, _
import logging
import base64
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz
from xlrd import open_workbook
import tempfile
_logger = logging.getLogger(__name__)


class MainImportInventory(models.Model):

    _inherit = 'product.category'
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
            
            return str(time_arr[hours]) + ":" + minutes          
    
    def import_data(self, part_master_id=False):
        if part_master_id:
            part_master = self.env[
                'import.inventory.master'].browse(part_master_id)
            total_success_import_record = 0
            total_failed_record = 0
            list_of_failed_record = ''
            datafile = part_master.file
            file_name = str(part_master.filename)
            category_obj = self.env['product.category']
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
                    # _logger.info("file_data")
                    # _logger.info(file_data)
                    fp = open(temp_path + '/xsl_file.xls', 'wb+')
                    fp.write(file_data)
                    fp.close()
                    wb = open_workbook(temp_path + '/xsl_file.xls')
                    data_list = []
                    header_list = []
                    headers_dict = {}
                    sheet_names = wb.sheet_names()
                    # _logger.info("list_of_failed_record")
                    # _logger.info(wb.sheets())
                    # xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
                    for sheet in wb.sheets():
                        # _logger.info(sheet.name)
                        if sheet.name == "دليل استرشادي ":
                            first_row = 0
                            item_code_row = 0
                            item_description_row = 0
                            main_account_row = 0
                            for rownum in range(sheet.nrows):
                                # _logger.info(rownum)
                                # _logger.info(sheet.row_values(rownum))
                                item = sheet.row_values(rownum)
                                # _logger.info(item)
                                if "الحساب الرئيسي " in item and "ITEM_CODE\nكود الصنف" in item:
                                    first_row = rownum
                                    # _logger.info("first_row")
                                    for idx1,item1 in enumerate(item):
                                        if "ITEM_CODE" in item1:
                                            item_code_row = idx1
                                        if "ITEM_DESCRIPTION" in item1:
                                            item_description_row = idx1
                                        if "الحساب الرئيسي " in item1:
                                            main_account_row = idx1
                                    break    
                            for rownum1 in range(sheet.nrows): 
                                item_y = sheet.row_values(rownum1)           
                                if rownum1 > first_row:
                                    item_code =  item_y[item_code_row]
                                    item_description = item_y[item_description_row] 
                                    main_account = item_y[main_account_row]     
                                    if item_code != "" and item_description != "" and main_account != "":
                                        try:
                                            # check if category exists:
                                            check_catId = self.env['product.category'].sudo().search([('name','=',main_account)])
                                            cat_id = False
                                            if check_catId:
                                                cat_id = check_catId.id
                                            else:    
                                                _logger.info('test')
                                                # create category
                                                parent_id_all = self.env['product.category'].sudo().search([('name','=','All')])
                                                category_vals = {
                                                    'name': main_account,
                                                    'parent_id': parent_id_all.id,
                                                }
                                                cat_id = self.env['product.category'].sudo().create(category_vals).id
                                            # check if product exists 
                                            check_productId = self.env['product.template'].sudo().search([('name','=',item_description)])
                                            if not check_productId:
                                                asset_cat = self.env['account.asset.category'].sudo().search([('name','=','الاصول الثابتة')])
                                                _logger.info(item_description)
                                                asset_category_id = False
                                                if asset_cat:
                                                    asset_category_id = asset_cat.id
                                                else:
                                                    asset_vals = {
                                                        'name': 'الاصول الثابتة',
                                                    }
                                                    asset_category_id = self.env['account.asset.category'].sudo().create(asset_vals).id
                                                _logger.info(check_productId)
                                                product_vals = {
                                                    'name': item_description,
                                                    'purchase_ok': True,
                                                    'sale_ok':False,
                                                    'categ_id':cat_id,
                                                    'asset_category_id':asset_category_id,
                                                    'type':'consu',
                                                    'list_price':0.0,
                                                    'default_code':item_code
                                                }
                                                self.env['product.template'].sudo().create(product_vals)
                                                total_success_import_record += 1
                                            else:
                                                total_failed_record += 1
                                                list_of_failed_record += "<h1>| Error at Line :" + str(rownum1 + 1) +"  => Product exist | </h1>" 
                                                _logger.error("<h1>| Error at Line :" + str(rownum1 + 1) +"  => Product exist | </h1>")   
                                        except Exception as e:    
                                            total_failed_record += 1
                                            list_of_failed_record += "<h1>| Error at Line :" + str(rownum1 + 1) + "   (" + str(e) + ") | </h1>" 
                                            _logger.error("Error at %s" % e)   
            except Exception as e1:
                list_of_failed_record += "<h1> | Error at Line : " + str(rownum1 + 1) + "    (" + str(e1) + ") | </h1>"


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
                self.env['import.inventory.history'].create({
                    'total_success_count': total_success_import_record,
                    'total_failed_count': total_failed_record,
                    'file': file_data,
                    'file_name': 'report_importazione.html',
                    'type': part_master.type,
                    'import_file_name': part_master.filename,
                    'start_date': start_date_in_user_tz,
                    'end_date': end_date_in_user_tz,
                    'operation': part_master.operation,
                })
                if part_master.user_id:
                    message = "Import process is completed. Check in Imported inventory History if all the inventory have" \
                              " been imported correctly. </br></br> Imported File: %s </br>" \
                              "Imported by: %s" % (
                                  part_master.filename, part_master.user_id.name)
                    part_master.user_id.notify_inventory_info(
                        message, part_master.user_id, sticky=True)
                self._cr.commit()
            except Exception as e:
                part_master.status = 'failed'
                _logger.error(e)
                self._cr.commit()
