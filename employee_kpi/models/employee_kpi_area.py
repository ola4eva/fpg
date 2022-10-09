from odoo import models, fields


class KpiKeyArea(models.Model):
    _name = "employee_kpi.assessment.area"
    _description = "Key Areas"
    
    name = fields.Char('Key Result Area')
