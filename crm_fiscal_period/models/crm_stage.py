from odoo import models, fields, api
from odoo.exceptions import UserError


class CrmStage(models.Model):
    _inherit = "crm.stage"

    user_notification_ids = fields.Many2many(
        'res.users', string='Notification Users')

    @api.constrains("is_close", "is_won")
    def _check_unique_close_won(self):
        if self.is_close and self.is_won:
            raise UserError("The same stage cannot be close and won!")
        if len(self.search([("is_close", "=", True)])) > 1:
            raise UserError("You can't have multiple close stages!")

    is_close = fields.Boolean("Is close stage?")
    mail_template_id = fields.Many2one('mail.template', string='Email Template', domain=[('model', '=', 'crm.stage')],
                                       help="If set, an email will be sent to the users added to a field that we will set.")

    def _notify_users(self, template_id, context={}):
        """Send notification to uses
        """
        for stage in self:
            if not template_id:
                template_id = stage.mail_template_id
            if not template_id:
                continue
            recipients = context.get(
                'recipients') or stage.user_notification_ids
            for recipient in recipients:
                if template_id:
                    ctx = dict(self._context)
                    ctx.update(recipient=recipient)
                    template_id.with_context(ctx).send_mail(
                        stage.id, force_send=True)
