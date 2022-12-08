from odoo import models, fields, api


class EmployeeKpiTemplate(models.Model):
    _name = "employee_kpi.kpi.template"
    _inherit = ['mail.thread', "mail.activity.mixin"]
    _description = "Kpi Template"

    name = fields.Char(string="Name", tracking=True, readonly=True, states={
                       'draft': [('readonly', False)]})
    user_id = fields.Many2one(
        "res.users", string="User", readonly=True, default=lambda self: self.env.uid)

    question_ids = fields.One2many(
        "employee_kpi.kpi.template.question", "template_id", string="Questions", readonly=True, states={'draft': [('readonly', False)]}
    )
    state = fields.Selection(
        [
            ("draft", "New"),
            ("open", "To Approve"),
            ("approve", "Approved"),
        ],
        string="State",
        default="draft",
        tracking=True,
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
    perspective_id = fields.Many2one(
        comodel_name="employee_kpi.perspective", string="Perspective")
    is_section = fields.Boolean(string="Is Section")
    target = fields.Float('Target')
    key_area = fields.Char(
        string="Key Result Area")
    template_id = fields.Many2one(
        "employee_kpi.kpi.template", string="Template", required=True)

    @api.constrains('weight')
    def _constrains_weight(self):
        for record in self:
            if record.weight <= 0:
                raise ValueError("Weight must be strictly positive")

    @api.constrains('target')
    def _constrains_target(self):
        for record in self:
            if record.target <= 0:
                raise ValueError("Target must be strictly positive")
            if record.target > 100:
                raise ValueError("Target cannot be greater than 100%")
