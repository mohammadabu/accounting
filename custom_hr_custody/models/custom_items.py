# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class HrCustomCustodyItems(models.Model):

    _name = 'hr.custody.items'
    _description = 'Hr Custody Items'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    @api.onchange('products','required_quantity')
    def onchange_products(self):
        current_id = self._origin.id   
        _logger.info("current_id")
        _logger.info(current_id)
        _logger.info("current_id")
        for rec in self:
            qty = 0
            qty_used = 0
            custody_used = 0
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
            _logger.info("---------stock_move-------------")
            custody_items = self.env['hr.custody.items'].sudo().search([('products','=',product_id),('id','!=',current_id)])
            _logger.info(custody_items)
            for item in custody_items:
                _logger.info(item)
                _logger.info(int(item.required_quantity))
                qty_used = qty_used + int(item.required_quantity)    
            _logger.info("---------stock_move-------------")



           # check custody used 
            _logger.info("---------custody used-------------")
            if current_id != False:
                custody_used_item = self.env['hr.custody.lines'].sudo().search([('custody_item','=',current_id),('custody_id.state','=','approved')])                
                _logger.info(custody_used_item)
                for used_item in custody_used_item:
                    custody_used = custody_used + int(used_item.custody_qty)
                    _logger.info(used_item.custody_qty)
            _logger.info("---------custody used-------------")

            this_required_quantity =  rec.required_quantity
            if qty < 0 :
               qty = 0 
            rec.quantity = qty
            rec.custody_quantity = qty_used
            rec.custody_used = custody_used
            rec.amount_remaining = qty - (qty_used + this_required_quantity)

    name = fields.Char(required=True)
    products = fields.Many2one('product.template')
    quantity = fields.Integer(compute="onchange_products")
    custody_quantity = fields.Integer(compute="onchange_products")
    custody_used = fields.Integer(compute="onchange_products")
    required_quantity = fields.Integer(required=True,default=1)
    amount_remaining = fields.Integer(compute="onchange_products")
    description = fields.Text()


    def write(self,values):
        rtn = super(HrCustomCustodyItems,self).write(values)
        required_quantity = int(self.required_quantity)
        custody_used = int(self.custody_used)
        amount_remaining = int(self.amount_remaining)
        _logger.info("---------write-------------")
        _logger.info(required_quantity)
        _logger.info(custody_used)
        _logger.info(amount_remaining)
        _logger.info("---------write-------------")
        if required_quantity < custody_used:
            raise exceptions.ValidationError(_('The required quantity is less than the quantity used'))
        elif amount_remaining < 0:
            raise exceptions.ValidationError(_('The remaining quantity is less than zero'))
        return rtn    

    @api.model
    def create(self,vals):
        required_quantity = 0
        custody_used = 0 
        amount_remaining = 0 
        rtn = super(HrCustomCustodyItems,self).create(vals)
        try:     
            required_quantity = rtn.required_quantity 
            custody_used = rtn.custody_used
            amount_remaining = rtn.amount_remaining
        except:
            required_quantity = 0
            custody_used = 0 
            amount_remaining = 0 
        if required_quantity < custody_used:
            raise exceptions.ValidationError(_('The required quantity is less than the quantity used'))
        elif amount_remaining < 0:
            raise exceptions.ValidationError(_('The remaining quantity is less than zero'))
        return rtn     


    def unlink(self):
        rtn = super(HrCustomCustodyItems, self).unlink()
        _logger.info("sasadsdasdasadsdadssadsda")
        _logger.info(self)
        _logger.info(rtn)
        # custody_used_item = self.env['hr.custody.lines'].sudo().search([('custody_item','=',current_id),('custody_id.state','=','approved')])                
        raise exceptions.ValidationError("dsadsa")
        return rtn    