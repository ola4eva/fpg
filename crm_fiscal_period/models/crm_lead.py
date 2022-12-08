from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import models, api, fields, Command, _
from odoo.exceptions import MissingError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    # notification_user_ids = fields.Many2many(
    #     comodel_name="res.users", string="Notified Users"
    # )

    @api.model
    def cron_close_leads(self):
        """Get all the leads that have not been closed at the end of the fiscal year and set them to close.

        # TODO: use the right domain
        1. Today's date is greater than the last day of the crm year
        2. Get all the leads in the fiscal year that are not in `won` state
        3. Close all these leads
        """
        crm_year_last_month = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("crm_fiscal_period.crm_year_last_month")
        )
        crm_year_last_day = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("crm_fiscal_period.crm_year_last_day")
        )
        crm_year_last_month = crm_year_last_month and int(crm_year_last_month)
        crm_year_last_day = crm_year_last_day and int(crm_year_last_day)
        crm_year_last_date = date(
            day=crm_year_last_day, month=crm_year_last_month, year=date.today().year
        )
        finalized_leads_to_close = self.env["crm.lead"].sudo()
        dt_now = datetime.now()
        this_year_end_date = last_fiscal_year_end_date = datetime.combine(
            crm_year_last_date, datetime.min.time()
        )
        if dt_now < this_year_end_date:
            last_fiscal_year_end_date = datetime.combine(
                crm_year_last_date +
                relativedelta(years=-1), datetime.min.time()
            )
        domain_expired = [("create_date", "<=", last_fiscal_year_end_date)]
        leads_to_close = self.search(domain_expired)
        for lead in leads_to_close:
            won_stages = self._stage_find(
                domain=[("is_won", "=", True)], limit=None)
            close_stages = self._stage_find(
                domain=[("is_close", "=", True)], limit=None
            )
            won_stage_id = next(
                (
                    stage
                    for stage in won_stages
                    if stage.sequence > lead.stage_id.sequence
                ),
                None,
            )
            if not won_stage_id:
                won_stage_id = next(
                    (
                        stage
                        for stage in reversed(won_stages)
                        if stage.sequence <= lead.stage_id.sequence
                    ),
                    won_stages,
                )
            close_stage_id = next(
                (
                    stage
                    for stage in close_stages
                    if stage.sequence > lead.stage_id.sequence
                ),
                None,
            )
            if not close_stage_id:
                close_stage_id = next(
                    (
                        stage
                        for stage in reversed(close_stages)
                        if stage.sequence <= lead.stage_id.sequence
                    ),
                    close_stages,
                )
            if lead.stage_id not in [close_stage_id, won_stage_id]:
                finalized_leads_to_close += lead
        finalized_leads_to_close.close()

    def _get_close_stage(self):
        """Return close stage"""
        for lead in self:
            limit = 1
            Stage = self.env["crm.stage"].sudo()
            domain = [("is_close", "=", True),
                      ("team_id", "=", lead.team_id.id)]
            close_stage = Stage.search(domain, limit=limit)
            if not close_stage:
                domain = [("is_close", "=", True)]
                close_stage = Stage.search(domain, limit=limit)
            return close_stage

    def close(self):
        for lead in self:
            close_stage = lead._get_close_stage()
            lead.write({"stage_id": close_stage.id, "active": False})
        return True

    # ---------------------------------------------------
    # Mail gateway
    # ---------------------------------------------------
    # remove because it was causing an error when `Won` button is clicked
    # def _track_template(self, changes):
    #     res = super(CrmLead, self)._track_template(changes)
    #     crm_lead = self[0]
    #     try:
    #         if "stage_id" in changes and crm_lead.stage_id.mail_template_id:
    #             stage_id = (
    #                 crm_lead.stage_id.mail_template_id,
    #                 {
    #                     "auto_delete_message": True,
    #                     "subtype_id": self.env["ir.model.data"]._xmlid_to_res_id(
    #                         "mail.mt_note"
    #                     ),
    #                     "email_layout_xmlid": "mail.mail_notification_light",
    #                 },
    #             )

    #             res["stage_id"] = stage_id
    #     except MissingError:
    #         pass
    #     finally:
    #         return res

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id:
            try:
                self.stage_id._notify_users(self.stage_id.mail_template_id, {
                    'recipients': self.stage_id.user_notification_ids})
            except MissingError:
                pass
