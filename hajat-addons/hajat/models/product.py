from odoo import models, fields, api # type: ignore
import requests # type: ignore
import logging
import base64

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        self.send_webhook(product, 'created')
        return product

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        for product in self:
            self.send_webhook(product, 'updated')
        return result

    def unlink(self):
        for product in self:
            self.send_webhook(product, 'deleted')
        result = super(ProductTemplate, self).unlink()
        return result
    def send_webhook(self, product, status):
        webhook_url = 'https://webhook.site/c2e3db55-1a90-4b40-94c4-db16d935bd95'
        data = {
            'id': product.id,
            'name': product.name,
            'list_price': product.list_price,
            'brand_id': product.brand_id.id if product.brand_id else None,  # Convert to ID
            'brand_name': product.brand_id.name if product.brand_id else None,  # Convert to Name
            'qty_available': product.qty_available,
            'public_categ_ids': [categ.name for categ in product.public_categ_ids] if product.public_categ_ids else [],  # Convert to list of names
            'uom_id': product.uom_id.id if product.uom_id else None,  # Convert to ID
            'uom_name': product.uom_id.name if product.uom_id else None,  # Convert to Name
            'status': status
        }
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send webhook for product {product.id} with status {status}: {e}")
