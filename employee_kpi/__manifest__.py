# -*- coding: utf-8 -*-
{
    'name': "Employee KPI",

    'summary': """
        Key Performance Indicators for FPG Employees""",

    'description': """
        Key Performance Indicators for FPG Employees
    """,
    
    'license': "LGPL-3",

    'author': "Olalekan Babawale",
    'website': "http://obabawale.github.io",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/employee_kpi_views.xml',
    ],
}
