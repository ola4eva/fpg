# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    sickle_cell_disease = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Sickle cell disease", copy=False)
    asthma = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Asthma", copy=False)
    hypertension = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Hypertension", copy=False)
    diabetes_mellitus = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Diabetes mellitus", copy=False)
    peptic_ulcer_disease = fields.Selection(selection=[(
        'yes', "Yes"), ('no', "No")], string="Peptic ulcer disease", copy=False)
    heart_disease = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Heart disease", copy=False)
    tuberculosis = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Tuberculosis", copy=False)
    epilepsy_seizure_disorder = fields.Selection(selection=[(
        'yes', "Yes"), ('no', "No")], string="Epilepsy/seizure disorder", copy=False)
    mental_illness = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Mental illness", copy=False)
    kidney_disease = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Kidney disease", copy=False)
    liver_disease = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Liver disease", copy=False)
    allergies = fields.Selection(selection=[(
        'yes', "Yes"), ('no', "No")], string="Allergies (including drug allergies)", copy=False)
    drug_addiction = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Drug addiction", copy=False)
    are_you_pregnant = fields.Selection(
        selection=[('yes', "Yes"), ('no', "No")], string="Are you pregnant", copy=False)
    condition_details = fields.Text(
        string='If yes to any/ some of the above, kindly give details')

    history_surgical_operation = fields.Selection(selection=[(
        'yes', "Yes"), ('no', "No")], string="Any history of surgical operation/ procedure", copy=False)
    history_surgical_operation_details = fields.Text(
        string='Kindly give details with date’s')

    presently_on_medication = fields.Selection(selection=[(
        'yes', "Yes"), ('no', "No")], string="Are you presently on medication", copy=False)
    presently_on_medication_details = fields.Text(
        string='Kindly give details including names of medication and dosages')

    admitted_health_facility_recently = fields.Selection(selection=[(
        'yes', "Yes"), ('no', "No")], string="Where you admitted in any health facility recently (one month prior to employment)", copy=False)
    admitted_health_facility_recently_details = fields.Text(
        string='Kindly give details including name of condition and health facility where you were treated')

    medical_emergency_contact = fields.Char(string='Medical Emergency Name')
    medical_emergency_address = fields.Text(string='Medical Emergency Address')
    medical_emergency_telephone = fields.Text(
        string='Medical Emergency Telephone')
    medical_emergency_email = fields.Text(string='Medical Emergency E- mail')
    submitted = fields.Boolean('Submitted')

    def action_submit(self):
        self.submitted = True

    @api.model
    def create(self, vals):
        res = super(HrEmployeePrivate, self).create(vals)
        res._restrict_employee_creation()
        return res

    def write(self, vals):
        res = super(HrEmployeePrivate, self).write(vals)
        self._restrict_employee_update()
        return res

    def _restrict_employee_creation(self):
        for rec in self:
            if not rec.user_has_groups('hr.group_hr_user'):
                raise UserError(
                    'You do not have rights to create/edit an Employee record(s), please contact HR')

    def _restrict_employee_update(self):
        for rec in self:
            if not rec.user_has_groups('hr.group_hr_user') and not rec.user_id.id == self.env.uid:
                raise UserError(
                    'You do not have rights to update other Employee record(s), please contact HR')
