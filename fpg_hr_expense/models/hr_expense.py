# -*- coding: utf-8 -*-
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    link = fields.Char(string='Link', compute="_compute_link",
                       help="A url representing the record on Odoo")

    def action_submit_sheet(self):
        try:
            self._notify_employee_manager()
        except Exception as e:
            _logger.error("%s" % e)
        return super(HrExpenseSheet, self).action_submit_sheet()

    def approve_expense_sheets(self):
        # send email to finance
        account_group = self.env.ref("account.group_account_invoice")
        email_template = self.env.ref(
            'fpg_hr_expense.hr_expense_sheet_submit_finance')
        account_users = account_group.users
        account_employees = self.env['hr.employee'].search(
            [('user_id', 'in', account_users.ids)])
        recipients = account_employees.read(['name', 'work_email'])
        _logger.info("RECIPIENTS %s" % recipients)
        for recipient in recipients:
            try:
                email_template.with_context({'recipient': recipient}).send_mail(
                    self.id, force_send=True)
            except:
                _logger.error("***** Error sending email to finance *****")
        return super(HrExpenseSheet, self).approve_expense_sheets()

    def _notify_employee_manager(self):
        """Notify the employee's manager that an expense report has been submitted for their review.
        """
        _logger.info("An expense report has been submitted for your review")
        email_template = self.env.ref(
            'fpg_hr_expense.hr_expense_sheet_submit_manager')
        return email_template.send_mail(self.id, force_send=True)

    def _compute_link(self):
        """Get the link to this record on odoo
        http://localhost:8069/web?debug=1#id=10&cids=1&model=hr.expense.sheet&view_type=form&menu_id=194
        """
        menu_id = self.env['ir.model.data']._xmlid_to_res_id(
            'hr_expense.menu_hr_expense_root')
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url') or self.get_base_url()
        link = f'{base_url}/web#id={self.id}&cids=1&model=hr.expense.sheet&view_type=form&menu_id={menu_id}'
        self.link = link
