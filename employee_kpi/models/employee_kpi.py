# -*- coding: utf-8 -*-

from urllib.parse import urlencode, urljoin
from odoo import models, fields, api

SELECTION_KPI = [
            ("draft", "New"),
            ("sent", "Sent To Employee"),
            ("manager", "Manager To Assess"),
            ("done", "Manager Assessed"),
        ]
class EmployeeKpi(models.Model):
    _name = "employee_kpi.employee_kpi"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "Employee Performance Assessment"

    def _get_default_user_id(self):
        return self.env.uid

    name = fields.Char(
        string="NAME",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="ASSIGNEE",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    department_id = fields.Many2one(
        "hr.department",
        string="UNIT",
        required=True,
        related="employee_id.department_id",
    )
    job_id = fields.Many2one(
        "hr.job",
        string="POSITION",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    period = fields.Char(
        string="PERIOD",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    parent_id = fields.Many2one(
        "hr.employee",
        string="REPORTING TO",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    user_id = fields.Many2one(
        "res.users", string="Responsible", default=_get_default_user_id
    )
    grade_level = fields.Char(
        "GRADE LEVEL",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    grade_months = fields.Integer(
        "MONTHS ON GRADE",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    kpi_type_id = fields.Many2one(
        "employee_kpi.employee_kpi.type",
        string="KPI TYPE",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    score_financial_perspective = fields.Float(
        "FINANCIAL PERSPECTIVE", compute="_compute_score_financial_perspective"
    )
    score_operations_perspective = fields.Float(
        "OPERATIONS PERSPECTIVE", compute="_compute_score_operations_perspective"
    )
    score_stakeholder_satisfaction_perspective = fields.Float(
        "STAKEHOLDER SATISFACTION",
        compute="_compute_score_stakeholder_satisfaction_perspective",
    )
    score_learning_growth_culture_perspective = fields.Float(
        "LEARNING GROWTH & CULTURE",
        compute="_compute_score_learning_growth_culture_perspective",
    )
    score_total = fields.Float(string="Total", compute="_compute_score_total")
    state = fields.Selection(
        SELECTION_KPI,
        string="State",
        default="draft",
        tracking=True,
    )
    question_ids = fields.One2many(
        "employee_kpi.question", "kpi_id", string="Questions"
    )
    template_id = fields.Many2one(
        comodel_name="employee_kpi.kpi.template",
        string="Template",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    exceptional_achievements = fields.Text("Exceptional Achievement(s)")
    areas_of_strength = fields.Text("Area of Strengths")
    job_improvement_recommendations = fields.Text("Job Improvement Recommendation(s)")
    appraiser_overall_comment = fields.Text("Appraiser's Overall Comment")
    appraisee_overall_comment = fields.Text("Appraisee's Overall Comment")
    fpg_final_recommendation = fields.Text("FPG's Final Recommendation")
    url = fields.Char("url", compute="_get_record_url")

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        value = {"value": {}}
        if self.employee_id:
            department_id = (
                self.employee_id.department_id and self.employee_id.department_id.id
            )
            job_id = self.employee_id.job_id and self.employee_id.job_id.id
            parent_id = self.employee_id.parent_id and self.employee_id.parent_id.id
            value["value"].update(
                {
                    "department_id": department_id,
                    "job_id": job_id,
                    "parent_id": parent_id,
                }
            )
        return value

    @api.onchange("template_id")
    def _onchange_template_id(self):
        if self.template_id:
            self.question_ids.unlink()
            Question = self.env["employee_kpi.question"].sudo()
            for question in self.template_id.question_ids:
                kpi_question = Question.create(
                    {
                        "key_area_id": question.key_area_id.id,
                        "perspective_id": question.perspective_id.id,
                        "name": question.name,
                        "weight": question.weight,
                        "target": question.target,
                        "is_section": question.is_section,
                    }
                )
                self.question_ids += kpi_question

    def action_send_to_employee(self):
        # send an email to employee
        template = self.env.ref("employee_kpi.employee_kpi_request_email_to_employee")
        template.send_mail(self.id, force_send=True)
        self.state = "sent"

    def action_send_to_manager(self):
        # send an email to manager
        template = self.env.ref(
            "employee_kpi.employee_kpi_request_email_to_employee_manager"
        )
        template.send_mail(self.id, force_send=True)
        self.state = "manager"

    def action_complete_assessment(self):
        # send notification to hr manager
        template = self.env.ref("employee_kpi.employee_kpi_completion_email_to_hr")
        template.send_mail(self.id, force_send=True)
        self.state = "done"

    def _get_record_url(self):
        base_url = self.get_base_url()
        params = {
            "id": self.id,
            "cids": self.id,
            "action": int(self.env.ref("employee_kpi.employee_kpi_action")),
            "model": self._name,
            "menu_id": int(self.env.ref("employee_kpi.employee_kpi_root_menu")),
            "view_type": "form",
        }
        url = f"{base_url}/web#{urlencode(params)}"
        self.url = url

    def _compute_score_financial_perspective(self):
        total = 0.0
        financial_perspective = self.env.ref("employee_kpi.perspective_financial")
        financial_perspective_kpis = self.question_ids.sudo().search(
            [("perspective_id", "=", financial_perspective.id)]
        )
        total = sum(financial_perspective_kpis.mapped("manager_final_score"))
        self.score_financial_perspective = total

    def _compute_score_operations_perspective(self):
        operations_perspective = self.env.ref("employee_kpi.perspective_operations")
        operations_perspective_kpis = self.question_ids.sudo().search(
            [("perspective_id", "=", operations_perspective.id)]
        )
        total = sum(operations_perspective_kpis.mapped("manager_final_score"))
        self.score_operations_perspective = total

    def _compute_score_stakeholder_satisfaction_perspective(self):
        stakeholders_perspective = self.env.ref("employee_kpi.perspective_stakeholders")
        stakeholders_perspective_kpis = self.question_ids.sudo().search(
            [("perspective_id", "=", stakeholders_perspective.id)]
        )
        total = sum(stakeholders_perspective_kpis.mapped("manager_final_score"))
        self.score_stakeholder_satisfaction_perspective = total

    def _compute_score_learning_growth_culture_perspective(self):
        growth_perspective = self.env.ref(
            "employee_kpi.perspective_learning_growth_culture"
        )
        growth_perspective_kpis = self.question_ids.sudo().search(
            [("perspective_id", "=", growth_perspective.id)]
        )
        total = sum(growth_perspective_kpis.mapped("manager_final_score"))
        self.score_learning_growth_culture_perspective = total

    def _compute_score_total(self):
        self.score_total = (
            self.score_financial_perspective
            + self.score_operations_perspective
            + self.score_stakeholder_satisfaction_perspective
            + self.score_learning_growth_culture_perspective
        )


class EmployeeKpiQuestion(models.Model):
    _name = "employee_kpi.question"
    _description = "Employee KPI Question"

    name = fields.Char(string="Key Performance Indicators", readonly=True, states={'draft': [('readonly', False)]})
    perspective_id = fields.Many2one(
        comodel_name="employee_kpi.perspective", string="Perspective", readonly=True, states={'draft': [('readonly', False)]}
    )
    key_area_id = fields.Many2one(
        "employee_kpi.assessment.area", string="Key Result Area", readonly=True, states={'draft': [('readonly', False)]}
    )
    weight = fields.Float("Weight", readonly=True, states={'draft': [('readonly', False)]})
    target = fields.Float("Target", readonly=True, states={'draft': [('readonly', False)]})
    self_rating = fields.Float("Self Rating", readonly=True, states={'sent': [('readonly', False)]})
    manager_rating = fields.Float("Manager's Rating", readonly=True, states={'manager': [('readonly', False)]})
    self_final_score = fields.Float(
        "Self Final Score", compute="_compute_self_final_score", readonly=True, states={'sent': [('readonly', False)]}
    )
    manager_final_score = fields.Float(
        "Manager's Final Score", compute="_compute_manager_final_score", readonly=True, states={'manager': [('readonly', False)]}
    )
    self_comment = fields.Char("Self Comment", readonly=True, states={'sent': [('readonly', False)]})
    manager_comment = fields.Char("Manager's Comment", readonly=True, states={'manager': [('readonly', False)]})
    kpi_id = fields.Many2one("employee_kpi.employee_kpi", string="KPI")
    is_section = fields.Boolean("Is Section")
    state = fields.Selection(string='State', related="kpi_id.state")
    
    def _compute_self_final_score(self):
        for record in self:
            try:
                record.self_final_score = (
                    record.self_rating * record.weight
                ) / record.target
            except ZeroDivisionError:
                record.self_final_score = 0

    def _compute_manager_final_score(self):
        for record in self:
            try:
                record.manager_final_score = (
                    record.manager_rating * record.weight
                ) / record.target
            except ZeroDivisionError:
                record.manager_final_score = 0

    @api.constrains("target")
    def _constrains_target(self):
        for record in self:
            if record.target > 100:
                raise ValueError("Target cannot exceed 100%")

    @api.constrains("self_rating")
    def _constrains_self_rating(self):
        for record in self:
            if record.self_rating > 100:
                raise ValueError("Self rating cannot exceed 100%")

    @api.constrains("manager_rating")
    def _constrains_manager_rating(self):
        for record in self:
            if record.self_rating > 100:
                raise ValueError("Manager rating cannot exceed 100%")
