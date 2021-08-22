{
    'name': 'Custom Etmam Permissions',
    'version': '13.0.1.0.0',
    'depends': ['hr', 'mail','hr_holidays','attend_data_import_xls'],
    'data': [
        'views/custom_permissions_view.xml',
        # 'views/custody_employee_view.xml',
        # 'views/custom_custody_view.xml',
        # 'views/custom_items_view.xml',
        'security/permissions_security.xml',
        'security/ir.model.access.csv',
    ],
}
