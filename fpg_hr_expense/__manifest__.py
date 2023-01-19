# -*- coding: utf-8 -*-
{
    'name': "HR Expense Mail Notifications",

    'summary': """
        Add email notifications to employee manager when an expense report is submitted""",

    'description': """
        Add email notifications to employee manager when an expense report is submitted. In the body of the email, add a link back to the record on odoo.
    """,

    'author': "Olalekan Babawale",
    'website': "http://obabawale.github.io",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['hr_expense'],

    'data': [
        'data/email_data.xml',
    ],
}
