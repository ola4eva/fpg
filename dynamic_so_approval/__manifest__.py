# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################
{
    'name': "Dynamic Purchase Approval",
    'category': 'Purchase',
    'version': '12.0.1.0',
    'author': 'Equick ERP',
    'description': """
        This module allows you to approve purchase order users or group wise.
    """,
    'summary': """Purchase Approval | Dynamic Purchase Approval | User wise purchase approval | multi user approval | multi user purchase approval | multi level approval | purchase multi level approval | dynamic approval|po approval | access rights wise po approval.""",
    'depends': ['base', 'purchase'],
    'price': 25,
    'currency': 'EUR',
    'license': 'OPL-1',
    'website': "",
    'data': [
        'security/ir.model.access.csv',
        'views/config_po_approval.xml',
        'views/purchase_order_view.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
