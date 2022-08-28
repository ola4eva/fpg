from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.model
    def cron_close_leads(self):
        leads_to_close = self.search([], limit=5)
        for lead in leads_to_close:
            lead.close()
