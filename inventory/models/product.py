from odoo import models, fields, api , _
from odoo.exceptions import ValidationError

class ProductLine(models.Model):
    _name = 'product.inventory.line'
    _description = 'Product Inventory Line'
    _inherit=['mail.thread','mail.activity.mixin']

    product_id = fields.Many2one(comodel_name="product.inventory", string=_("Products"), required=False, )
    measurement_types = fields.Selection(string=_("Measurement Type"), required=False, related="product_id.measurement_type",)
    quantity = fields.Float(string=_("Quantity"),default=1)
    date_of_receipt = fields.Date(string=_("Date of Receipt"), required=False, )
    expiration_date = fields.Date(string=_("Expiration Date"), required=False, )
    cost = fields.Float(string=_("Cost"),  required=False, )
    total_cost = fields.Float(string=_("Total Cost"), required=False, compute="_compute_total_cost",)
    pay = fields.Float(string=_("Pay"), required=False, )
    difference = fields.Float(string=_("Difference"), required=False, readonly=True, store=True,compute="_compute_difference",)

    vendor_id = fields.Many2one(comodel_name="vendor.inventory", string=_("Vendor"), required=False, )

    @api.depends("cost","quantity")
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = (rec.cost or 0.0) * (rec.quantity or 0.0)
    @api.depends("pay", "total_cost")
    def _compute_difference(self):
        for rec in self:
            rec.difference = (rec.pay or 0.0) - (rec.total_cost or 0.0)


class Product(models.Model):
    _name = 'product.inventory'
    _description = 'Product Inventory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string=_("Product Name"), required=False, )
    measurement_type = fields.Selection(string=_("Measurement Type"), selection=[('milliliter', _('Milli Liter')),('liter', _('Liter')),('kilogram', _('Kilogram')),('gram', _('Gram')),('unit', _('Unit')),], required=True, default="milliliter")
    consumption = fields.Float(string=_("Consumption"),  required=False, )
    total_quantity = fields.Float(string=_("Total Quantity"), compute="_compute_total_quantity", store=True)


    vendors_ids = fields.One2many(comodel_name="product.inventory.line", inverse_name="product_id", string=_("Vendors"), required=False, )

    @api.depends('vendors_ids.quantity', 'consumption')
    def _compute_total_quantity(self):
        for rec in self:
            total_qty = sum(line.quantity for line in rec.vendors_ids)
            rec.total_quantity = total_qty - (rec.consumption or 0.0)







@api.constrains('total_quantity')
def _check_name(self):
    for rec in self:
        if rec.total_quantity <= 0:
            raise ValidationError(_("⚠️ Total Quantity should be positive number\n consumption is not True"))
