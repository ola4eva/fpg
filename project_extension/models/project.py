# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class Project(models.Model):
    _inherit = "project.project"
    percent_progress = fields.Float(
        string="Progress", copy=False, compute="_compute_percent_progress"
    )

    @api.depends('task_ids')
    def _compute_percent_progress(self):
        for project in self:
            percent_progress = 0.0
            if project.task_ids:
                total_number_of_tasks = len(project.task_ids)
                total_number_of_completed_tasks = len(
                    project.task_ids.filtered(lambda task: task.stage_id.is_closed))
                percent_progress = (
                    total_number_of_completed_tasks / total_number_of_tasks) * 100
            project.percent_progress = percent_progress


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def _notify_task_overdue(self):
        """Send mail notifying of tasks that are overdue"""
        today = fields.Date.today()
        today_to_string = fields.Date.to_string(today)
        domain_overdue = [
            ("date_deadline", "<", today_to_string),
            ("stage_id.is_closed", "=", False),
        ]
        overdue_tasks = self.search(domain_overdue)
        sender_email = self.env.ref(
            'base.user_admin').email
        for task in overdue_tasks:
            assignees = task.user_ids
            days_overdue = (today - task.date_deadline).days
            mail_template = self.env.ref(
                "project_extension.task_overdue")
            for assignee in assignees:
                partner_id = assignee.partner_id
                mail_template.with_context(recipient=partner_id, days_overdue=days_overdue, sender_email=sender_email).send_mail(
                    task.id, force_send=True
                )
        return True

    @api.model
    def _notify_task_will_due(self):
        """Send notification to assignee for tasks that are due in some days."""
        today = fields.Date.today()
        one_day = today + relativedelta(days=1)
        two_days = today + relativedelta(days=2)
        three_days = today + relativedelta(days=3)
        five_days = today + relativedelta(days=5)

        # Get the domains for one day, two days, three days and five days
        domain_one_day = [
            ("stage_id.is_closed", "=", False),
            ("date_deadline", "=", one_day),
        ]
        domain_two_days = [
            ("stage_id.is_closed", "=", False),
            ("date_deadline", "=", two_days),
        ]
        domain_three_days = domain_two_days = [
            ("stage_id.is_closed", "=", False),
            ("date_deadline", "=", three_days),
        ]
        domain_five_days = domain_two_days = [
            ("stage_id.is_closed", "=", False),
            ("date_deadline", "=", five_days),
        ]
        tasks_due_in_one_day = self.search(domain_one_day)
        tasks_due_in_two_days = self.search(domain_two_days)
        tasks_due_in_three_days = self.search(domain_three_days)
        tasks_due_in_five_days = self.search(domain_five_days)
        mail_template_one_day = self.env.ref(
            "project_extension.task_due_in_one_day")
        mail_template_two_days = self.env.ref(
            "project_extension.task_due_in_two_days")
        mail_template_three_days = self.env.ref(
            "project_extension.task_due_in_three_days")
        mail_template_five_days = self.env.ref(
            "project_extension.task_due_in_five_days")

        sender_email = self.env.ref(
            'base.user_admin').email

        # send the emails depending on when the tasks are expected to be due
        # TODO: enhance the implementation later as this approach is not DRY and efficient
        for task in tasks_due_in_one_day:
            for assignee in task.user_ids:
                mail_template_one_day.with_context(recipient=assignee.partner_id, sender_email=sender_email).send_mail(
                    task.id, force_send=True
                )
        for task in tasks_due_in_two_days:
            for assignee in task.user_ids:
                mail_template_two_days.with_context(recipient=assignee.partner_id, sender_email=sender_email).send_mail(
                    task.id, force_send=True
                )
        for task in tasks_due_in_three_days:
            for assignee in task.user_ids:
                mail_template_three_days.with_context(recipient=assignee.partner_id, sender_email=sender_email).send_mail(
                    task.id, force_send=True
                )
        for task in tasks_due_in_five_days:
            for assignee in task.user_ids:
                mail_template_five_days.with_context(recipient=assignee.partner_id, sender_email=sender_email).send_mail(
                    task.id, force_send=True
                )
        return True
