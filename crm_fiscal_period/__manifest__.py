# -*- coding: utf-8 -*-
{
    'name': "CRM Fiscal Period",

    'summary': """
        Manage CRM Fiscal Year""",

    'description': """
        Manage CRM Fiscal Year
    """,

    'author': "Olalekan Babawale",
    'website': "http://www.yourcompany.com",

    'category': 'CRM',
    'version': '15.1.0',

    'depends': ['crm', 'mail'],

    'data': [
        'data/email_data.xml',
        'data/ir_cron_data.xml',
        'views/res_config_settings_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
    ],
    'license': 'LGPL-3',
}
