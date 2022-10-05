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

    'depends': ['base', 'hr_payroll', 'hr_payroll_account'],

    'data': [
        'security/ir.model.access.csv',
        'views/payroll_adjustment_views.xml',
        'wizard/payroll_register_view.xml',
    ],
}
