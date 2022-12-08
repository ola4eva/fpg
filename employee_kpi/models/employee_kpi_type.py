from odoo import models, fields


class EmployeeKpiType(models.Model):
    _name = "employee_kpi.employee_kpi.type"
    _description = "Employee Performance Assessment Type"

    name = fields.Char(string="Name")
