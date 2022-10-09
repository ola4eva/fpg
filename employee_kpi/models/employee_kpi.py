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
    state = fields.Selection(
        [
            ("draft", "New"),
            ("confirm", "Employee Assessed"),
            ("approve", "Manager Assessed"),
        ],
        string="State",
        default="draft",
    )

    def action_submit(self):
        pass


class EmployeeKpiQuestion(models.Model):
    _name = "employee_kpi.question"
    _description = "Employee KPI Question"

    # perspective_id = fields.Many2one('employee_kpi.perspective', string='perspective')
    perspective = fields.Char("Perspective")
    # key_result_area = fields.Char("Key Result Area")
    key_area_id = fields.Many2one('employee_kpi.assessment.area', string='Key Result Area') 
    kpi = fields.Char(string="Key performance Indicators")
    weight = fields.Float("weight")
    self_rating = fields.Float("Self Rating")
    manager_rating = fields.Float("Manager's Rating")
    self_final_score = fields.Float("Self Final Score")
    manager_final_score = fields.Float("Manager's Final Score")
    self_comment = fields.Char("Self Comment")
    manager_comment = fields.Char("Manager's Comment")


