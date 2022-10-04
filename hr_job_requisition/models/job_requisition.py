# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class JobRequisition(models.Model):
    _name = "hr_job_requisition.job_requisition"
    _description = "HR Job Requisition"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", readonly=True, default="/")
    description = fields.Char(string="Description")
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
    number_vacancy = fields.Integer(
        "Number of vacancies",
        help="""Number of Jobs in this Role in the Department/Branch""",
    )
    address = fields.Char(string="Location/Address")
    parent_job_id = fields.Many2one(comodel_name="hr.job", string="Reports To")
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
        string="Classification",
    )
    date_hire = fields.Date("Date to Hire By")
    state = fields.Selection(
        [
            ("draft", "New"),
            ("open", "To approve"),
            ("approve", "HR To Approve"),
            ("done", "Approved"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        string="state",
        default="draft",
        readonly=True,
        tracking=True,
    )

    # A
    critical_task_ids = fields.One2many(
        comodel_name="hr_job_requisition.key.task",
        inverse_name="requisition_id",
        string="Critical Tasks",
    )

    # B.
    key_skill_ids = fields.One2many(
        comodel_name="hr_job_requisition.key.skill",
        inverse_name="requisition_id",
        string="Key Skills",
    )

    # C.
    have_direct_reports = fields.Selection(
        [
            ("yes", "Yes"),
            ("no", "No"),
        ],
        string="Have direct reports?",
    )
    number_reports = fields.Integer("Number of Reports")
    number_report_levels = fields.Integer("Numberof levels of Reports")

    # D. Provide information regarding the position’s qualifications including those most critical to a successful hire.
    education = fields.Char("Education")
    experience = fields.Char("Experience")
    certifications = fields.Char("Certifications/Licenses")
    skill_ids = fields.Many2many("hr.skill", string="Skills")
    special_equipment_used = fields.Char("Special Equipment Used")
    special_working_conditions = fields.Char("Special Working Conditions")
    other_qualifications = fields.Char("Others")

    # E. Service Details
    full_or_part_time = fields.Selection(
        [
            ("part_time", "Part Time"),
            ("full_time", "Full Time"),
        ],
        string="Service Details",
    )
    full_time_equivalent = fields.Float("Full Time Equivalent")
    hours_per_week = fields.Integer("Anticipated Number of Hours/Week")
    length_of_service = fields.Char(
        "Anticipated Length of Service (for temporary hires)"
    )
    requested_start_date = fields.Date("Requested Start Date")

    # F. Compensation Planning
    min_salary = fields.Float("min_salary")
    max_salary = fields.Float("min_salary")
    salary_grade = fields.Char("Salary Grade (if applicable)")

    # G. Budget information and business justifications for filling the position (please be detailed and specific)
    budget_annual_salary = fields.Float("Annual Salary")
    benefits = fields.Float("Benefits")
    other_expenses = fields.Float(
        string="Other anticipated expenses in filling this position (costs of hiring, training, new equipment,"
    )
    # H. Type of Action:
    action_type = fields.Selection(
        [
            ("new", "New"),
            ("replacement", "Replacement"),
            ("reallocation", "Reallocation of Resources"),
            ("budgeted", "Budgeted"),
            ("non_budgeted", "Non-budgeted"),
        ],
        string="Type of Action",
    )

    exit_employee_id = fields.Many2one("hr.employee", string="Exiting employee")
    exit_date = fields.Date(string="Exit Date")
    exit_reason = fields.Char(
        string="If this is a replacement position, please describe who is leaving, when and why."
    )
    reallocation_details = fields.Char("Reallocation Details")
    coping_strategy_vacant_position = fields.Char(string="How is work getting done?")
    impact_left_vacant = fields.Char(
        string="What is the impact on the company if this position is left vacant?"
    )
    distributable_among_others = fields.Selection(
        [
            ("yes", " Yes"),
            ("no", " No"),
        ],
        string="Could the work be distributed among other positions instead of filling this position?",
    )
    filled_by_less_experience = fields.Selection(
        [
            ("yes", " Yes"),
            ("no", " No"),
        ],
        string="Could the position be filled by a less skilled, less experienced, and less expensive employee?",
    )
    performed_by_part_time = fields.Selection(
        [
            ("yes", "Yes"),
            ("no", "No"),
        ],
        string="Could a part time or temporary employee perform the tasks of this position?",
    )
    revenue_impact = fields.Char("Revenue")
    customer_service_impact = fields.Char("Customer Service")
    other_functions_impact = fields.Char("Other Critical Company Functions")

    # I. List any other information that might be helpful in the recruitment and hiring for this position.
    other_recruitment_info_ids = fields.One2many(
        "hr_job_requisition.recruitment.info",
        "requisition_id",
        string="Other Recruitment Information",
    )

    # J. Approvals
    hiring_manager_id = fields.Many2one(
        "hr.employee", string="Hiring Manager", copy=False
    )
    date_submitted = fields.Date(string="Date", copy=False)
    hiring_manager_job_id = fields.Many2one("hr.job", string="Position", copy=False)
    supervisor_id = fields.Many2one(
        "hr.employee", string="Supervisor of Hiring Manager", copy=False
    )
    date_approved = fields.Date(string="Date", copy=False)
    supervisor_job_id = fields.Many2one("hr.job", string="Position", copy=False)
    hr_approver_id = fields.Many2one(
        "hr.employee", string="Human Resource Manager", copy=False
    )
    date_hr_approved = fields.Date(string="Date", copy=False)
    hr_manager_job_id = fields.Many2one("hr.job", string="Position", copy=False)
    job_position_id = fields.Many2one(
        comodel_name="hr.job", string="Job Position", copy=False
    )

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].sudo().next_by_code("job.requisition")
        return super().create(vals)
    
    def action_view_job_positions(self):
        return {
            'name': _('Job Positions'),
            'view_mode': 'form',
            'res_model': 'hr.job',
            'view_id': self.env.ref('hr.view_hr_job_form').id,
            'type': 'ir.actions.act_window',
            'res_id': self.job_position_id.id,
        }

    def action_submit(self):
        employee_id = (
            self.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", self.env.user.id)], limit=1)
        )
        job_id = employee_id and employee_id.job_id
        self.update(
            {
                "hiring_manager_id": employee_id and employee_id.id or False,
                "hiring_manager_job_id": job_id and job_id.id or False,
                "date_submitted": date.today(),
                "state": "open",
            }
        )
        return True

    def action_approve(self):
        employee_id = (
            self.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", self.env.user.id)], limit=1)
        )
        job_id = employee_id and employee_id.job_id
        self.update(
            {
                "supervisor_id": employee_id and employee_id.id or False,
                "supervisor_job_id": job_id and job_id.id or False,
                "date_approved": date.today(),
                "state": "approve",
            }
        )
        return True

    def action_hr_approve(self):
        employee_id = (
            self.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", self.env.user.id)], limit=1)
        )
        job_id = employee_id and employee_id.job_id

        HrJob = self.env["hr.job"].sudo()
        job_position_id = None
        try:
            job_position_id = HrJob.create(
                {
                    "name": self.description,
                    "expected_employees": self.number_vacancy,
                    # "number_of_recruitment": self.number_vacancy,
                    "address_id": self.env.user.company_id.id,
                    "department_id": self.department_id and self.department_id.id,
                    "user_id": employee_id
                    and employee_id.user_id
                    and employee_id.user_id.id
                    or False,
                }
            )
        except Exception as e:
            _logger.error(f"Error {e} while creating Job Position")
        else:
            self.job_position_id = job_position_id and int(job_position_id)
            _logger.info(f"Job {job_position_id.name} was created successfully")
        self.update(
            {
                "hr_approver_id": employee_id and employee_id.id or False,
                "hr_manager_job_id": job_id and job_id.id or False,
                "date_hr_approved": date.today(),
                "state": "done",
            }
        )

    def action_reject(self):
        self.state = "reject"

    def action_cancel(self):
        self.state = "cancel"


class OtherRecruitmentInfo(models.Model):
    _name = "hr_job_requisition.recruitment.info"
    _description = "Other Useful Recruitment Information"
    _table = "recruitment_info"

    name = fields.Char(string="Name")
    requisition_id = fields.Many2one(
        "hr_job_requisition.job_requisition", string="Requisition"
    )


class JobRequisitionSkill(models.Model):
    _name = "hr_job_requisition.key.skill"
    _description = "Key Skills"
    _table = "job_requisition_skill"

    name = fields.Char(string="Name")
    requisition_id = fields.Many2one(
        "hr_job_requisition.job_requisition", string="Requisition"
    )


class JobRequisitionTask(models.Model):
    _name = "hr_job_requisition.key.task"
    _description = "Critical Tasks"
    _table = "job_requisition_task"

    name = fields.Char(string="Name")
    requisition_id = fields.Many2one(
        "hr_job_requisition.job_requisition", string="Requisition"
    )


class HrSkill(models.Model):
    _name = "hr.skill"
    _description = "Relevant Skills"

    name = fields.Char(string="Skill")
