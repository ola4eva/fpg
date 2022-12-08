# -*- coding: utf-8 -*-
{
    'name': "Employee Profile",

    'summary': """
        Employee Ext Module (My Profile).""",

    'description': """
        this module is designed to extend employee module 
    """,

    'author': "Olalekan Babawale",
    'website': "http://obabawale.github.io",
    'license': 'LGPL-3',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': [
        'base',
        'hr',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
    ],
}