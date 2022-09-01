from datetime import date
from odoo import models, api, fields
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def cron_close_leads(self):
        td = date.today()
        day, month, year = td.day, td.month, td.year
        if month == 1:
            pass
        
        leads_to_close = self.search([], limit=5)
        # TODO: use the right domain
        """
        1. Today's date is greater than the last day of the crm year
        2. Get all the leads in the fiscal year that are not in `won` state
        3. Close all these leads  
        """
        leads_to_close.close()

    def close(self):
        for lead in self:
            print("&&&&&&&&&&&&& Processing lead %s " % lead.name)
            limit = 1
            Stage = self.env["crm.stage"].sudo()
            domain = [("is_close", "=", True), ("team_id", "=", lead.team_id.id)]
            close_stage = Stage.search(domain, limit=limit)
            if not close_stage:
                domain = [("is_close", "=", True)]
                close_stage = Stage.search(domain, limit=limit)
            lead.stage_id = close_stage.id
            lead.active = False
        return True 


class CrmStage(models.Model):
    _inherit = "crm.stage"

    @api.constrains("is_close", "is_won")
    def _check_seats_limit(self):
        if self.is_close and self.is_won:
            raise UserError("The same stage cannot be close and won!")
        if len(self.search([("is_close", "=", True)])) > 1:
            raise UserError("You can't have multiple close stages!")

    is_close = fields.Boolean("Is close stage?")
