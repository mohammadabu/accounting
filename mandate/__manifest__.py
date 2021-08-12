{
    'name': 'Custom Etmam Mandate',
    'version': '13.0.1.0.0',
    'depends': ['hr', 'mail','hr_holidays'],
    'data': [
        'views/custom_mandate_view.xml',
        'security/mandate_security.xml',
        'security/ir.model.access.csv',
    ],
}
