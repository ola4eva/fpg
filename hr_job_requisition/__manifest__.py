# -*- coding: utf-8 -*-
{
    'name': "HR Job Requisition",

    'summary': """
        Job requisition""",

    'description': """
        Job requisition
    """,

    'author': "FPG Technologies Ltd",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'hr'],

    'data': [
        'security/access_groups.xml',
        'security/ir.model.access.csv',
        'views/job_requisition_views.xml',
    ],
}
