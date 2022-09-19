# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrDutyAssumption(models.Model):
    _name = "hr_duty_assumption.hr_duty_assumption"
    _description = "HR Assumption of Duty"

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
    # pfa_name= fields.Char(string="", )
    
    # TODO
    # 1. Add chatter to the form view
    # 2. Add menu for pfa's
    # 3. Add fuctionality to object methods
    # 4. Clean up the form view
    
    state = fields.Selection(
        [
            ("draft", "New"),
            ("submit", "To Validate"),
            ("validate", "To approve"),
            ("approve", "Approved"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        string="State",
        readonly=True,
        default="draft",
    )

    def action_submit(self):
        pass

    def action_validate(self):
        pass

    def action_approve(self):
        pass

    def action_cancel(self):
        pass

    def action_reject(self):
        pass


class PensionAdministrator(models.Model):
    _name = "hr_duty_assumption.pfa"
    _description = "Pension Fund Administrator"

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    website = fields.Char("Website")
    phone = fields.Char(string="Phone Number")
