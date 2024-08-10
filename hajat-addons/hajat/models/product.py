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
        # image_base64 = product.image_1920 and base64.b64encode(product.image_1920).decode('utf-8') or None
        webhook_url = 'https://webhook.site/fccac2e2-56f4-47b9-9a90-937ccf2f952f'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        data = {
            'id': product.id,
            'name': product.name,
            'default_code': product.default_code,
            'list_price': product.list_price,
            'description': product.description_sale,
            'image': f"{base_url}/api/product/{product.id}/image",
            'category': product.categ_id.name,
            'type': product.type,
            'status': status
        }
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send webhook for product {product.id} with status {status}: {e}")
