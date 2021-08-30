{
    'name': 'Custom Etmam Custody',
    'version': '13.0.1.0.0',
    'depends': ['hr', 'mail', 'om_account_asset', 'product'],
    'data': [
        'security/custody_security.xml',
        'views/wizard_reason_view.xml',
        'views/custody_employee_view.xml',
        'views/custom_custody_view.xml',
        'views/custom_items_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
