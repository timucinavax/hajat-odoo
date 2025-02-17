from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    longitude = fields.Float(string='Longitude')
    latitude = fields.Float(string='Latitude')
    is_verified = fields.Boolean(string="Is Verified", default=False)
