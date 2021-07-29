{
    'name': 'Product Data Import - XLSX',
    'version': '13.0.0.1.0',
    'depends': ["stock","web_notify","om_account_asset"],
    'data': [
        'wizard/import_product_data_view.xml',
        'views/import_product_history_view.xml',
        'views/import_product_master_view.xml',
        'security/ir.model.access.csv',
    ],
}
