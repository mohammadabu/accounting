{
    'name': 'Odoo Customization',
    'version': '13.0.1.0.0',
    'depends': ['base','hr','hr_holidays','hr_attendance','hr_expense'],
    'data': [
        'views/hr_employee_view.xml',
        'security/groups.xml',
        'security/security.xml',
        'security/ir.model.access.csv'
    ],
}
