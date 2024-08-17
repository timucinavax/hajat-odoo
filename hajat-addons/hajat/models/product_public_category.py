from odoo import models, fields, api
import requests
import logging
from ..shared.config import config

_logger = logging.getLogger(__name__)

class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    @api.model
    def create(self, vals):
        category = super(ProductPublicCategory, self).create(vals)
        self.send_webhook(category, 'created')
        return category

    def write(self, vals):
        result = super(ProductPublicCategory, self).write(vals)
        for category in self:
            self.send_webhook(category, 'updated')
        return result

    def unlink(self):
        for category in self:
            self.send_webhook(category, 'deleted')
        result = super(ProductPublicCategory, self).unlink()
        return result

    def send_webhook(self, category, status):
        _logger.info(f"Sending webhook for product category {category.id} with status {status}")

        webhook_url = f'{config.backend_webhook_url}/api/categories/webhook'
        data = {
            'id': category.id,
            'name': category.name,
            'parentId': category.parent_id.id if category.parent_id else None,
            'status': status
        }

        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send webhook for product category {category.id} with status {status}: {e}")
