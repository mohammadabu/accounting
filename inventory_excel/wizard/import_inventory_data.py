from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz
import logging
_logger = logging.getLogger(__name__)


class ImportInventory(models.TransientModel):

    _name = 'import.inventory'
    _description = "Import Inventory"

    name = fields.Char('File name')
    file = fields.Binary('File')
    state = fields.Selection([('init', 'init'), ('done', 'done')],
                             string='Status', readonly=True, default='init')
    type = fields.Selection([("xlsx", "XLSX")],
                            default="xlsx", string="File type.")
    operation = fields.Selection(
        [('create', 'Create Record'), ('update', 'Update Record')],
        default='create')

    def import_data_through_cron(self):
        # asset_type = self.env['account.asset.category'].sudo().search([],limit=1)
        # if len(asset_type) > 0:
        #     asset_type = asset_type.id
        # else:
        #     asset_type = False      
        # category_id = 4 #فئات المنتج
        # product_master = self.env['product.template'].create({
        #     'name': 'ألات تصوير',
        #     'sale_ok': False,
        #     'purchase_ok': True,
        #     'can_be_expensed': False,
        #     'type': 'consu',
        #     'categ_id': 4,
        #     'list_price': 0.0,
        #     'asset_category_id': asset_type,
        # })
        # _logger.info('asset_type')
        # _logger.info(asset_type)
        self.ensure_one()
        cron_obj = self.env['ir.cron']
        now_time = datetime.now() + timedelta(seconds=1)
        attendances_master = self.env['import.inventory.master'].create({
            'file': self.file,
            'filename': self.name,
            'type': self.type,
            'file_updated': True,
            'user_id': self._uid,
            'status': 'in_process',
            'operation': self.operation,
        })

        user_tz = self.env.user.tz or str(pytz.utc)
        local = pytz.timezone(user_tz)
        user_time_zone = datetime.strftime(pytz.utc.localize(
            datetime.strptime(datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S'),
                              DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),
            DEFAULT_SERVER_DATETIME_FORMAT)

        # self.state = 'done'
        self.pool.get("product.template").import_data(self,attendances_master.id)
        return {
            'name': _('Import Attendances'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.inventory',
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }     

