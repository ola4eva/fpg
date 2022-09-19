# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JobRequisition(models.Model):
    _name = "hr_job_requisition.job_requisition"
    _description = "HR Job Requisition"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    type = fields.Selection(
        [
            ("temporary", "Temporary Hire"),
            ("regular", "Regular Hire"),
        ],
        string="Type of Action",
        default="regular",
    )
    job_id = fields.Many2one("hr.job", string="Position/title")
    department_id = fields.Many2one("hr.department", string="Department")
    management_level = fields.Integer("Management Level")
    number_vacancy = fields.Integer("Number of vacancies")
    classification = fields.Selection(
        [
            ("strategic_leadership", "Strategic Leadership"),
            ("business_leadership", "Business Leadership"),
            ("manager", "Manager"),
            ("certified_professional", "Certified Professional"),
            ("professional", "Professional"),
            ("generalist", "Generalist"),
            ("support", "Support"),
        ],
        string="classification",
    )

    date_hire = fields.Date("Date to Hire By")
    have_direct_reports = fields.Selection(
        [
            ("yes", "Yes"),
            ("no", "No"),
        ],
        string="Have direct reports?",
    )

    state = fields.Selection(
        [
            ("draft", "New"),
            ("open", "To approve"),
            ("approve", "Approved"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        string="state",
        default="draft",
        readonly=True,
        tracking=True,
    )
    
    def action_submit(self):
        self.state = 'open'
    
    def action_approve(self):
        self.state = 'approve'
    
    def action_reject(self):
        self.state = 'reject'
    
    def action_cancel(self):
        self.state = 'cancel'