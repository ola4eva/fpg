from odoo import models, fields


class KpiKeyArea(models.Model):
    _name = "employee_kpi.assessment.area"
    _description = "Key Areas"

    name = fields.Char("Key Result Area")
    perspective_id = fields.Many2one("employee_kpi.perspective", string="Perspective")


class KpiPerspective(models.Model):
    _name = "employee_kpi.perspective"
    _description = "Perspective"

    name = fields.Char("Perspective Area")
