# -*- coding: utf-8 -*-
{
    'name': "Assumption of Duty",

    'summary': """
        Assumption of Duty""",

    'description': """
        Assumption of Duty
    """,

    'author': "FPG Technologies & Solutions Ltd",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'hr', 'hr_payroll'],

    'data': [
        'security/access_groups.xml',
        'security/ir.model.access.csv',
        'data/email_data.xml',
        'views/duty_assumption_views.xml',
    ],
}
