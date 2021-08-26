# -*- coding: utf-8 -*-
{
    'name': "Employee Dashboard",
    'version': '13.0',
    'depends': ['hr', 'hr_holidays', 'hr_timesheet', 'hr_attendance','project','project_privacy_visibility'],
    'external_dependencies': {
        'python': ['pandas'],
    },
    'data': [
        'security/ir.model.access.csv',
        'report/broadfactor.xml',
        'views/dashboard_views.xml',
    ],
    'qweb': ["static/src/xml/hrms_dashboard.xml"],
    'images': ["static/description/banner.gif"],
}
