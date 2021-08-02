# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class HrCustomCustodyItems(models.Model):

    _name = 'hr.custody.items'
    _description = 'Hr Custody Items'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char()
    products = fields.Many2one('product.template')
    quantity = fields.Char()
    custody_quantity = fields.Char()
    amount_remaining = fields.Char()
    description = fields.Text()
    