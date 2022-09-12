from odoo import models, fields

CRM_MONTHS = [
    ("1", "January"),
    ("2", "February"),
    ("3", "March"),
    ("4", "April"),
    ("5", "May"),
    ("6", "June"),
    ("7", "July"),
    ("8", "August"),
    ("9", "September"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December"),
]


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    crm_year_last_month = fields.Selection(selection=CRM_MONTHS, string="Last Month", default='12', config_parameter="crm_fiscal_period.crm_year_last_month")
    crm_year_last_day = fields.Char(string="Last Day", default=31, config_parameter="crm_fiscal_period.crm_year_last_day")
