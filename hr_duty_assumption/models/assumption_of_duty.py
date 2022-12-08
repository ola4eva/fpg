# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class HrDutyAssumption(models.Model):
    _name = "hr_duty_assumption.hr_duty_assumption"
    _description = "HR Assumption of Duty"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    employee_number = fields.Char("Employee Number")

    # position / grade
    position = fields.Char("Position/Grade Appointed")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    unit = fields.Char(string="Unit")
    job_id = fields.Many2one(comodel_name="hr.job", string="Position")
    salary_offered = fields.Float("Salary Offered")
    date_assumption = fields.Date(string="Date Assumed Duty")
    place = fields.Char(string="Place of Assumption")
    supervisor_id = fields.Many2one(comodel_name="hr.employee", string="Supervisor")
    bank_ids = fields.Many2many("res.partner.bank", string="Account Numbers")
    pension_info_ids = fields.One2many(
        comodel_name="hr_duty_assumption.pension.information",
        inverse_name="duty_assumption_id",
        string="Pension Information",
    )
    date_assume_duty_bank = fields.Date('Date Assumed Duty With Bank')
    letter_of_appointment_date = fields.Date('Letter of Appointment Date')
    user_id = fields.Many2one('res.users', string='User')
    date_submitted = fields.Date('Date')

    state = fields.Selection(
        [
            ("draft", "New"),
            ("submit", "To Approve"),
            ("approve", "Approved"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected")
        ],
        string="State",
        readonly=True,
        default="draft",
        tracking=True,
    )

    def action_submit(self):
        email_template = self.env.ref("hr_duty_assumption.submit_email")
        group_hr_payroll_offier = self.env.ref('hr_duty_assumption.group_manager')
        recipients = group_hr_payroll_offier.users.mapped('partner_id')
        ctx = self.env.context.copy()
        ctx['recipients'] = recipients
        try:
            email_template.with_context(ctx).send_mail(self.id, force_send=True)
        except:
            _logger.error("Unable to send duty assumption email")
        return self.update(
            {
                "state": "submit",
            }
        )
        
        
    def action_approve(self):
        # send an email to payroll officer
        email_template = self.env.ref("hr_duty_assumption.approve_email")
        group_hr_payroll_offier = self.env.ref('hr_payroll.group_hr_payroll_user')
        recipients = group_hr_payroll_offier.users.mapped('partner_id')
        ctx = self.env.context.copy()
        ctx['recipients'] = recipients
        try:
            email_template.with_context(ctx).send_mail(self.id, force_send=True)
        except:
            _logger.error("Unable to send duty assumption email")
        return self.update(
            {
                "state": "approve",
                "date_submitted": date.today(),
                "user_id": self.env.user.id,
            }
        )

    def action_cancel(self):
        self.update({"state": "cancel"})
        
    def action_reject(self):
        self.update({"state": "reject"})


class PensionFundDetails(models.Model):
    _name = "hr_duty_assumption.pension.information"
    _description = "Pension Fund Information"

    pfa_id = fields.Many2one(
        "pension.fund.administrator", string="Pension Fund Adminstrator"
    )
    start_date = fields.Date("start_date")
    reg_no = fields.Char("RSA Number")
    duty_assumption_id = fields.Many2one(
        comodel_name="hr_duty_assumption.hr_duty_assumption",
        string="Assumption of Duty",
    )


class PensionAdministrator(models.Model):
    _name = "pension.fund.administrator"
    _description = "Pension Fund Administrator"

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    website = fields.Char("Website")
    phone = fields.Char(string="Phone Number")
