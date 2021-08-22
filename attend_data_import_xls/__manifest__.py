{
    'name': 'Attend Data Import - XLS',
    'version': '13.0.0.1.0',
    'depends': ["hr_attendance","web_notify"],
    'data': [
        'views/hr_attendance.xml',
        'wizard/import_attendances_data_view.xml',
        'views/import_attendances_history_view.xml',
        'views/import_attendances_master_view.xml',
        'views/reason_modification.xml',
        'security/ir.model.access.csv',
        # 'data/data.xml', 
    ],
}
