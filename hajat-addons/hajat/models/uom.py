from odoo import models, api
import requests
import logging
from ..shared.config import config

_logger = logging.getLogger(__name__)


class UoM(models.Model):
    _inherit = 'uom.uom'

    @api.model
    def create(self, vals):
        uom = super(UoM, self).create(vals)
        self.send_webhook(uom, 'created')
        return uom

    def write(self, vals):
        result = super(UoM, self).write(vals)
        for uom in self:
            self.send_webhook(uom, 'updated')
        return result

    def unlink(self):
        for uom in self:
            self.send_webhook(uom, 'deleted')
        result = super(UoM, self).unlink()
        return result

    def send_webhook(self, uom, status):
        if(uom.category_id.id != 1):
            return
        _logger.info(f"Sending webhook for UoM {uom.id} with status {status}")
        webhook_url = f'{config.backend_webhook_url}/api/uoms/webhook'
        data = {
            'id': uom.id,
            'name': uom.name,
            "ratio":uom.ratio,
            'status': status
        }

        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send webhook for UoM {uom.id} with status {status}: {e}")
