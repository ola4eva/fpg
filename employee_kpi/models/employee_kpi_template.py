from odoo import models, fields


class EmployeeKpiTemplate(models.Model):
    _name = "employee_kpi.kpi.template"
    _description = "Kpi Template"

    name = fields.Char(string="Name")
    user_id = fields.Many2one("res.users", string="User")

    question_ids = fields.One2many(
        "employee_kpi.kpi.template.question", "template_id", string="Questions"
    )
    state = fields.Selection(
        [
            ("draft", "New"),
            ("open", "To Approve"),
            ("approve", "Approved"),
        ],
        string="State",
        default="draft",
    )

    def action_submit(self):
        self.state = "open"

    def action_approve(self):
        self.state = "approve"


class EmployeeKpiQuestion(models.Model):
    _name = "employee_kpi.kpi.template.question"
    _description = "Employee KPI Template Question"

    name = fields.Char(string="Key Performance Indicators", required=True)
    weight = fields.Float("Weight")
    perspective = fields.Char("Perspective")
    is_section = fields.Boolean(string="Is Section")
    key_area_id = fields.Many2one(
        "employee_kpi.assessment.area", string="Key Result Area"
    )
    template_id = fields.Many2one("employee_kpi.kpi.template", string="Template", required=True)
