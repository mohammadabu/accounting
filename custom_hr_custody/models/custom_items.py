# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class HrCustomCustodyItems(models.Model):

    _name = 'hr.custody.items'
    _description = 'Hr Custody Items'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.onchange('products','required_quantity')
    def onchange_products(self):        
        qty = 0
        qty_used = 0
        this_required_quantity = 0
        for rec in self:
            # check product inventory qty 
            product_id = rec.products.id
            stock_move = self.env['stock.move.line'].sudo().search([('state','=','done'),('product_id','=',product_id)])
            for line in stock_move:
                qty = qty + int(line.qty_done)
            # check product custody qty
            custody_items = self.env['hr.custody.items'].sudo().search([('products','=',product_id)])
            for item in custody_items:
                qty_used = qty_used + int(item.required_quantity)    
            this_required_quantity =  rec.required_quantity
            qty_used = qty_used - this_required_quantity
            if qty < 0 :
               qty = 0 
        self.quantity = qty
        self.custody_quantity = qty_used
        self.amount_remaining = custody_quantity + this_required_quantity

    name = fields.Char()
    products = fields.Many2one('product.template')
    quantity = fields.Integer(compute="onchange_products")
    custody_quantity = fields.Integer(compute="onchange_products")
    required_quantity = fields.Integer(required=True,default=1)
    amount_remaining = fields.Integer(compute="onchange_products")
    description = fields.Text()

