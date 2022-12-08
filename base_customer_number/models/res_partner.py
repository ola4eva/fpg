# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class base_customer_number(models.Model):
    _inherit = "res.partner"

    customer_number = fields.Char("Customer ID")

    @api.constrains("customer_number")
    def _constrains_customer_number(self):
        Partner = self.env["res.partner"]
        partners_with_current_customer_number = (
            Partner.search(
                [("customer_number", "=", self.customer_number)]) - self
        )
        if partners_with_current_customer_number and self.customer_number:
            raise UserError("The customer must be strictly unique!")
