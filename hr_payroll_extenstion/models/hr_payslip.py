from odoo import models, api


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    @api.model
    def create(self, vals):
        payslip = super().create(vals)
        HrPayslipInput = self.env['hr.payslip.input'].sudo()
        HrPayslipInputType = self.env['hr.payslip.input.type'].sudo()
        if not vals.get("input_line_ids"):
            for input_type in HrPayslipInputType.search([]):
                HrPayslipInput.create({
                    'input_type_id': input_type.id,
                    'amount': 0.0,
                    'payslip_id': payslip.id
                })
        return payslip
