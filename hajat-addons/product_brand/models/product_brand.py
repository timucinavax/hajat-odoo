from odoo import models, fields

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'
    _order = 'sequence, name'

    name = fields.Char('Brand Name', required=True)
    image = fields.Binary('Image')
    sequence = fields.Integer('Sequence', default=10)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Brand')
