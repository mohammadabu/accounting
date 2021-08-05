{
    'name': 'Custodian Receipt Form',
    'version': '13.0.0.0',
    'depends': ['base','hr','custom_hr_custody'],
    'data': [
        'views/hr_custody.xml',
        'views/action_manager.xml',
        'data/custodian_receipt_report_data.xml',
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
    ],
}