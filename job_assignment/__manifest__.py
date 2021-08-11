{
    'name': 'Custom Etmam Job Assignment',
    'version': '13.0.1.0.0',
    'depends': ['hr', 'mail','hr_holidays'],
    'data': [
        'views/custom_job_assignment_view.xml',
        'data/data.xml',
        # 'views/custody_employee_view.xml',
        # 'views/custom_custody_view.xml',
        # 'views/custom_items_view.xml',
        # 'security/custody_security.xml',
        'security/ir.model.access.csv',
    ],
}
