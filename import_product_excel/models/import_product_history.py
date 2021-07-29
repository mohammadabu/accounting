from odoo import models, fields


class ImportProductHistory(models.Model):

    _name = 'import.product.history'
    _description = "Import Product History"

    total_success_count = fields.Integer('Success')
    total_failed_count = fields.Integer('Failed')
    file = fields.Binary('File')
    file_name = fields.Char('File Name')
    import_file_name = fields.Char('Imported File Name')
    start_date = fields.Char('Import Start At')
    end_date = fields.Char('Import End At')
    type = fields.Selection([("csv", "CSV"), ("xlsx", "XLSX")],
                            default="csv", string="File type.")
    operation = fields.Selection(
        [('create', 'Create Record'),
         ('update', 'Update Record')],
        default='create')
