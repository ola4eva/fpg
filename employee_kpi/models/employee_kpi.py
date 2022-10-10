# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeKpi(models.Model):
    _name = "employee_kpi.employee_kpi"
    _description = "Employee Performance Assessment"

    def _get_default_user_id(self):
        return self.env.uid

    def _get_default_employee_id(self):
        employee_id = (
            self.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", self._get_default_user_id())], limit=1)
        )
        return employee_id

    def _get_default_department_id(self):
        employee_id = self._get_default_employee_id()
        return employee_id and employee_id.department_id

    def _get_default_job_id(self):
        employee_id = self._get_default_employee_id()
        return employee_id and employee_id.job_id

    def _get_default_employee_manager_id(self):
        employee_id = self._get_default_employee_id()
        return employee_id and employee_id.parent_id

    name = fields.Char(string="NAME")
    employee_id = fields.Many2one(
        "hr.employee", string="ASSIGNEE", default=_get_default_employee_id
    )
    department_id = fields.Many2one(
        "hr.department", string="UNIT", default=_get_default_department_id
    )
    job_id = fields.Many2one("hr.job", string="POSITION", default=_get_default_job_id)
    period = fields.Char(string="PERIOD")
    parent_id = fields.Many2one(
        "hr.employee", string="REPORTING TO", default=_get_default_employee_manager_id
    )
    grade_level = fields.Char("GRADE LEVEL")
    grade_months = fields.Integer("MONTHS ON GRADE")
    kpi_type_id = fields.Many2one("employee_kpi.employee_kpi.type", string="KPI TYPE")
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
        [
            ("draft", "New"),
            ("confirm", "Employee Assessed"),
            ("approve", "Manager Assessed"),
        ],
        string="State",
        default="draft",
    )
    question_ids = fields.One2many(
        "employee_kpi.question", "kpi_id", string="Questions"
    )
    template_id = fields.Many2one(
        comodel_name="employee_kpi.kpi.template", string="Template"
    )
    exceptional_achievements = fields.Text("Exceptional Achievement(s)")
    areas_of_strength = fields.Text("Area of Strengths")
    job_improvement_recommendations = fields.Text("Job Improvement Recommendation(s)")
    appraiser_overall_comment = fields.Text("Appraiser's Overall Comment")
    appraisee_overall_comment = fields.Text("Appraisee's Overall Comment")
    fpg_final_recommendation = fields.Text("FPG's Final Recommendation")

    def action_submit(self):
        pass

    def _compute_score_financial_perspective(self):
        total = 0.0
        financial_perspective = self.env.ref("employee_kpi.perspective_financial")
        financial_perspective_kpis = self.question_ids.sudo().search([(
            'perspective_id', '=', financial_perspective.id
        )])
        total = sum(financial_perspective_kpis.mapped('manager_final_score'))
        print("$$$$$$$$$$$$$$$$$$$$$$$", total)
        self.score_financial_perspective = total

    def _compute_score_operations_perspective(self):
        operations_perspective = self.env.ref("employee_kpi.perspective_operations")
        operations_perspective_kpis = self.question_ids.sudo().search([(
            'perspective_id', '=', operations_perspective.id
        )])
        total = sum(operations_perspective_kpis.mapped('manager_final_score'))
        self.score_operations_perspective = total

    def _compute_score_stakeholder_satisfaction_perspective(self):
        stakeholders_perspective = self.env.ref("employee_kpi.perspective_stakeholders")
        stakeholders_perspective_kpis = self.question_ids.sudo().search([(
            'perspective_id', '=', stakeholders_perspective.id
        )])
        total = sum(stakeholders_perspective_kpis.mapped('manager_final_score'))
        self.score_stakeholder_satisfaction_perspective = total

    def _compute_score_learning_growth_culture_perspective(self):
        growth_perspective = self.env.ref("employee_kpi.perspective_learning_growth_culture")
        growth_perspective_kpis = self.question_ids.sudo().search([(
            'perspective_id', '=', growth_perspective.id
        )])
        total = sum(growth_perspective_kpis.mapped('manager_final_score'))
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

    name = fields.Char(string="Key performance Indicators")
    perspective_id = fields.Many2one(
        comodel_name="employee_kpi.perspective", string="Perspective"
    )
    key_area_id = fields.Many2one(
        "employee_kpi.assessment.area", string="Key Result Area"
    )
    weight = fields.Float("Weight")
    target = fields.Float('Target')
    self_rating = fields.Float("Self Rating")
    manager_rating = fields.Float("Manager's Rating")
    self_final_score = fields.Float("Self Final Score", compute="_compute_self_final_score")
    manager_final_score = fields.Float("Manager's Final Score", compute="_compute_manager_final_score")
    self_comment = fields.Char("Self Comment")
    manager_comment = fields.Char("Manager's Comment")
    kpi_id = fields.Many2one("employee_kpi.employee_kpi", string="KPI")
    is_section = fields.Boolean("Is Section")
    
    def _compute_self_final_score(self):
        for record in self:
            try:
                record.self_final_score = (record.self_rating * record.weight) / record.target
            except ZeroDivisionError:
                record.self_final_score = 0
            
    def _compute_manager_final_score(self):
        for record in self:
            try:
                record.manager_final_score = (record.manager_rating * record.weight) / record.target
            except ZeroDivisionError:
                record.manager_final_score = 0
                
    @api.constrains('target')
    def _constrains_target(self):
        for record in self:
            if record.target > 100:
                raise ValueError("Target cannot exceed 100%")
            
    @api.constrains('self_rating')
    def _constrains_self_rating(self):
        for record in self:
            if record.self_rating > 100:
                raise ValueError("Self rating cannot exceed 100%")
            
    @api.constrains('manager_rating')
    def _constrains_manager_rating(self):
        for record in self:
            if record.self_rating > 100:
                raise ValueError("Manager rating cannot exceed 100%")
