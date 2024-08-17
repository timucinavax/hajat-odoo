from odoo import models, fields

class Banner(models.Model):
    _name = 'banner'
    _description = 'Banner'
    _order = 'sequence, id'

    image = fields.Binary('Image')
    sequence = fields.Integer('Sequence', default=10)
