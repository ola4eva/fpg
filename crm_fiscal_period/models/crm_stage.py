from odoo import models, fields, api
from odoo.exceptions import UserError


class CrmStage(models.Model):
    _inherit = "crm.stage"
    
    @api.constrains("is_close", "is_won")
    def _check_seats_limit(self):
        if self.is_close and self.is_won:
            raise UserError("The same stage cannot be close and won!")
        if len(self.search([("is_close", "=", True)])) > 1:
            raise UserError("You can't have multiple close stages!")

    is_close = fields.Boolean("Is close stage?")
    mail_template_id = fields.Many2one('mail.template', string='Email Template', domain=[('model', '=', 'crm.stage')],
        help="If set, an email will be sent to the users added to a field that we will set.")
     