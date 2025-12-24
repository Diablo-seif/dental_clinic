from odoo import models, fields, api , _

class Vendor(models.Model):
    _name = 'vendor.inventory'
    _description = 'Vendor Inventory'
    _inherit=['mail.thread','mail.activity.mixin']

    name = fields.Char(string=_("Vendor Name"), required=True, tracking=True)
    company_name = fields.Char(string=_("Company Name"), tracking=True)

    phone = fields.Char(string=_("Fist Number"),default='+20 1',tracking=True)

    products_ids = fields.One2many(comodel_name="product.inventory.line", inverse_name="vendor_id", string=_("Products"), required=False, )
