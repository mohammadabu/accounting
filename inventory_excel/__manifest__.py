{
    'name': 'Inventory Data Import - XLS',
    'version': '13.0.0.1.0',
    'depends': ["stock","web_notify"],
    'data': [
        #'views/hr_attendance.xml',
        'wizard/import_inventory_data_view.xml',
        'views/import_inventory_history_view.xml',
        'views/import_inventory_master_view.xml',
        'security/ir.model.access.csv',
        # 'data/data.xml', 
    ],
}
