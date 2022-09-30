# -*- coding: utf-8 -*-
{
    'name': "HR Payroll Extension",

    'summary': """
        Extension to Payroll Module""",

    'description': """
        Add payroll register and automatically populate other inputs fields when payroll is generated.
    """,

    'author': "Olalekan Babawale",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'hr_payroll'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
