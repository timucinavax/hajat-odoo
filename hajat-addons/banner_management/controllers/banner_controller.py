from odoo import http
from odoo.http import request
import base64

class BannerController(http.Controller):
    PLACEHOLDER_IMAGE_BASE64 = "data:image/jpeg;base64,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"

    @http.route('/api/banner/<int:banner_id>/image', type='http', auth='public')
    def get_banner_image(self, banner_id, **kwargs):
        banner = request.env['banner'].sudo().browse(banner_id)
        if not banner or not banner.exists() or not banner.image:
            return self._get_placeholder_image()

        image_base64 = banner.image
        image_data = base64.b64decode(image_base64)
        headers = [
            ('Content-Type', 'image/png'), 
            ('Content-Length', len(image_data))
        ]
        return request.make_response(image_data, headers=headers)

    def _get_placeholder_image(self):
        image_data = base64.b64decode(self.PLACEHOLDER_IMAGE_BASE64.split(",")[1])
        headers = [
            ('Content-Type', 'image/jpeg'),  # Change the content type if needed
            ('Content-Length', len(image_data))
        ]
        return request.make_response(image_data, headers=headers)
