from odoo import models, fields, api
import requests
import logging
from ..shared.config import config

_logger = logging.getLogger(__name__)

class ProductBrand(models.Model):
    _inherit = 'product.brand'

    @api.model
    def create(self, vals):
        brand = super(ProductBrand, self).create(vals)
        self.send_webhook(brand, 'created')
        return brand

    def write(self, vals):
        result = super(ProductBrand, self).write(vals)
        for brand in self:
            self.send_webhook(brand, 'updated')
        return result

    def unlink(self):
        for brand in self:
            self.send_webhook(brand, 'deleted')
        result = super(ProductBrand, self).unlink()
        return result

    def send_webhook(self, brand, status):
        webhook_url = f'{config.backend_webhook_url}/api/brands/webhook'
        data = {
            'id': brand.id,
            'name': brand.name,
            'status': status
        }
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send webhook for product brand {brand.id} with status {status}: {e}")

