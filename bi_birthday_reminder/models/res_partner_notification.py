from datetime import datetime, timedelta
from odoo import models, api, fields


def convert_config_to_days(rs):
    if rs.period_unit == 'days':
        return rs.period
    elif rs.period_unit == 'weeks':
        return rs.period * 7
    elif rs.period_unit == 'months':
        return rs.period * 30


class PartnerNotification(models.TransientModel):

    _name = 'res.partner.notification'
    _description = 'Birthday Advance Notification'

    name = fields.Char()

    @api.model
    def _cron_upcoming_birthday_notification(self):
        recipient = {}
        recipient['name'] = "Alabi Adebayo"
        customers = self.env['res.partner'].sudo().search(
            [('birthdate', '!=', False)])
        email_template = self.env.ref(
            'bi_birthday_reminder.email_template_upcoming_birthday_notification')
        notification_configs = self.env['res.partner.notification.config'].sudo().search([
        ])
        notification_schedule_in_days = [
            convert_config_to_days(x) for x in notification_configs]
        ctx = self._context.copy()
        today = datetime.today()
        for notification_schedule in notification_schedule_in_days:
            # notify customers whose birthdays fall on the schedule
            target_date = today + timedelta(days=int(notification_schedule))
            filtered_customers = customers.filtered(
                lambda customer: customer.birthdate.month == target_date.month and customer.birthdate.day == target_date.day)
            if not filtered_customers:
                continue
            rec = self.create({})
            ctx.update(
                recipient=recipient,
                days_ahead=notification_schedule,
                customers_with_upcoming_birthdays=filtered_customers
            )
            email_template.with_context(ctx).send_mail(rec.id)
        return True


class BirthdayNotificationConfig(models.Model):
    _name = 'res.partner.notification.config'
    _description = 'Partner Advance Notification Configuration'

    # name = fields.Char(string='Name')
    period = fields.Integer(string="")
    period_unit = fields.Selection(selection=[
        ('days', "Days"),
        ('weeks', "Weeks"),
        ('months', "Months"),
    ], string="Unit")
