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

    'depends': ['base', 'hr', 'hr_recruitment'],

    'data': [
        'security/access_groups.xml',
        'security/ir.model.access.csv',
        'data/email_data.xml',
        'data/ir_sequence.xml',
        'views/job_requisition_views.xml',
    ],
    'license': 'LGPL-3',
}
