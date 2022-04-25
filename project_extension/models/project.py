# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil import relativedelta


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    # field_name = fields.Boolean('field_name')
    
    def _onchange_stage_id(self):
        if self.stage_id.is_closed:
            # send mail to the assignee stating that the project has been closed
            pass
        
    def _notify_to_due_project(self):
        # send mail notifying of projects that will be due in days
        pass
    
    def _notify_of_due_project(self):
        # send mail to assignee stating overdue projects
        domain = [('stage_id.is_closed', '=', False)]
        pass
    

class ProjectTask(models.Model):
    _inherit = 'project.task'
        
    def _onchange_stage_id(self):
        if self.stage_id.is_closed:
            for user in self.user_ids:
                # send mail to the assignee stating that the project has been closed
                pass
            pass
        
    @api.model
    def _notify_task_overdue(self):
        # send mail notifying of projects that will be due in days
        today = fields.Date.today()
        today_to_string = fields.Date.to_string(today)
        domain_overdue = [('date_deadline', '<', today_to_string), ('stage_id.is_closed', '=', False)]
        overdue_tasks = self.search(domain_overdue)
        for task in overdue_tasks:
            print ("**************************************")
            print ("** Task: ** ", task.name, "; ** Due Date: **", task.date_deadline)
            assignees = task.user_ids
            mail_template = self.env.ref("project_extension.task_one_day_overdue")
            for assignee in assignees:
                partner_id = assignee.partner_id
                mail_template.with_context(recipient=partner_id).send_mail(task.id, force_send=True)
        return True
    
    def _notify_of_due_project(self):
        # send mail to assignee stating overdue projects
        domain = [('stage_id.is_closed', '=', False)]
        pass
    