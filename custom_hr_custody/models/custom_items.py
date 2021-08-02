# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class HrCustomCustodyItems(models.Model):

    _name = 'hr.custody.items'
    _description = 'Hr Custody Items'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    @api.model
    def getItemQuantity(self):
        product_id = self.products.id
        stock_move = self.env['stock.move.line'].sudo().search([('state','=','done'),('product_id','=',product_id)])
        qty = 0
        for line in stock_move:
            qty = qty + int(line.qty_done)
        self.quantity = qty

    name = fields.Char()
    products = fields.Many2one('product.template')
    quantity = fields.Integer(compute='getItemQuantity')
    custody_quantity = fields.Char()
    amount_remaining = fields.Char()
    description = fields.Text()
    