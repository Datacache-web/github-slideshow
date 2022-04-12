# -*- coding: utf-8 -*-

# imports of python
import hashlib, os
# imports of odoo 
from odoo import fields, models, api

# inherit the res.partner table add fields
class ResPartner(models.Model):
    _inherit = "res.partner"
    
    #   onchange method to generate encryption key 
    @api.onchange('expiry_date', 'email', 'product_code') 
    def _onchange_expiry_date(self):
        for rec in self:
            if rec.expiry_date and rec.product_code and rec.email:
                encrypt_key = str(rec.expiry_date) + str(rec.product_code) + str(rec.email)           
                key_salt = os.urandom(32).hex()
                key = hashlib.sha1()
                key.update(('%s%s' % (key_salt, encrypt_key)).encode('utf-8'))
                product_key = key.hexdigest()
                rec.encryption_key = product_key
            else:
                rec.encryption_key = ''
    
    
    renewal_date = fields.Date("Renewal Date")
    user_limit = fields.Integer("User Limit")
    expiry_date = fields.Date("Expiry Date")
    product_code = fields.Char("Product Code")
    active_box = fields.Boolean("Active")
    encryption_key = fields.Char("Encryption Key")
    validity_status = fields.Selection([('valid', 'Valid'),('not valid', 'Not Valid')],string="Validity Status", default='valid')
    
    