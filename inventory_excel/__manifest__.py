{
    'name': 'Product Data Import - XLS',
    'version': '13.0.0.1.0',
    'depends': ["stock","web_notify"],
    'data': [
        'wizard/import_product_data_view.xml',
        'views/import_product_history_view.xml',
        'views/import_product_master_view.xml',
        'security/ir.model.access.csv',
    ],
}
