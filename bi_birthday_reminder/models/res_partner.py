# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing
# details.

from datetime import datetime, timedelta
from odoo import SUPERUSER_ID
from odoo import api, fields, models, _
from odoo.http import request


class res_partner(models.Model):

    _inherit = "res.partner"

    birthdate = fields.Date(string='Date Of Birth')

    def send_birthday_reminder(self):
        for partner in self:
            if not partner.birthdate:
                continue
            today = datetime.today()
            if not (partner.birthdate.month == today.month and partner.birthdate.day == today.day):
                continue
            email_template = self.env.ref(
                "bi_birthday_reminder.email_template_edi_birthday_reminder")
            email_template.send_mail(partner.id, force_send=True)

    @api.model
    def _cron_birthday_reminder(self):
        partners = self.search([('birthdate', '!=', False)])
        today = datetime.today()
        partners = partners.filtered(
            lambda partner: partner.birthdate.month == today.month and partner.birthdate.day == today.day)
        return partners.send_birthday_reminder()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
