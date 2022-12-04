# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': "FPG Base Module",
    'version': "15.0.0.0",
    'category': "Security",
    "license": 'LGPL-3',
    'summary': 'Base for managing user groups',
    'description': '''
        Add access group for MD/CEO
    ''',
    "author": "Olalekan Babawale",
    'website': 'https://obabawale.github.io',
    'depends': ['base'],
    'data': [
        'security/fpg_base_groups.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
