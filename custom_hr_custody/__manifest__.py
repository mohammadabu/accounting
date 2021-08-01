{
    'name': 'Custom Etmam Custody',
    'version': '13.0.1.0.0',
    'depends': ['hr', 'mail', 'om_account_asset', 'product'],
    'data': [
        'security/custody_security.xml',
        'views/wizard_reason_view.xml',
        # 'views/custody_view.xml',
        'views/custom_custody_view.xml',
        'views/custom_items_view.xml',
        # 'views/hr_employee_view.xml',
        # 'views/notification_mail.xml',
        # 'reports/custody_report.xml'
        'security/ir.model.access.csv',
    ],
    # 'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
