# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import logging
_logger = logging.getLogger(__name__)

class HrCustomCustodyItems(models.Model):

    _name = 'hr.custody.items'
    _description = 'Hr Custody Items'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.onchange('products','required_quantity')
    def onchange_products(self):        
        for rec in self:
            qty = 0
            qty_used = 0
            this_required_quantity = 0
            # check product inventory qty 
            product_id = rec.products.id
            stock_move = self.env['stock.move.line'].sudo().search([('state','=','done'),('product_id','=',product_id)])
            _logger.info("---------stock_move-------------")
            for line in stock_move:
                _logger.info(int(line.qty_done))
                qty = qty + int(line.qty_done)
            _logger.info("---------stock_move-------------")    

            # check product custody qty
            cust_id = self.id or 0
            _logger.info("---------stock_move-------------")
            custody_items = self.env['hr.custody.items'].sudo().search([('products','=',product_id),('id','!=',cust_id)])
            _logger.info(custody_items)
            for item in custody_items:
                if item.id != cust_id:
                    _logger.info(int(item.required_quantity))
                    qty_used = qty_used + int(item.required_quantity)    
            _logger.info("---------stock_move-------------")
            this_required_quantity =  rec.required_quantity
            if qty < 0 :
               qty = 0 
            rec.quantity = qty
            # rec.custody_quantity = qty_used - this_required_quantity
            rec.custody_quantity = qty_used
            # rec.amount_remaining = qty - (qty_used + this_required_quantity)
            rec.amount_remaining = this_required_quantity + (qty_used - this_required_quantity)

    name = fields.Char()
    products = fields.Many2one('product.template')
    quantity = fields.Integer(compute="onchange_products")
    custody_quantity = fields.Integer(compute="onchange_products")
    required_quantity = fields.Integer(required=True,default=1)
    amount_remaining = fields.Integer(compute="onchange_products")
    description = fields.Text()

