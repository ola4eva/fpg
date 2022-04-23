# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    field_name = fields.Boolean('field_name')
    