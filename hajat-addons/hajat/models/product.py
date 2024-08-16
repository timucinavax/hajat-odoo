from odoo import models, fields, api # type: ignore
import requests # type: ignore
import logging
from ..shared.config import config

import os
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
        if not product.brand_id:
            return
        _logger.info(f"Sending webhook for product {product.id} with status {status} {config.backend_webhook_url}")
        webhook_url = f'{config.backend_webhook_url}/api/products/webhook'
        data = {
            'id': product.id,
            'name': product.name,
            'qty_available': product.qty_available,
            'description': product.description_sale,
            'list_price': product.list_price,
            'categoryId': product.public_categ_ids[0].id if product.public_categ_ids else None,
            'brandId': product.brand_id.id if product.brand_id else None,
            'uomId': product.uom_id.id if product.uom_id else None, 
            'status': status
        }
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send webhook for product {product.id} with status {status}: {e}")
