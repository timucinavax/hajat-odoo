from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class ContactController(http.Controller):
    @http.route('/custom_contact/api/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_contact(self, **kwargs):
        # Log received data
        _logger.info("Received data: %s", json.dumps(kwargs))

        # Extract data from the request
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')

        # Check if mandatory fields are provided
        if not name or not email:
            return {'error': 'Name and email are required'}

        # Create a new contact
        contact = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
        })

        return {'success': True, 'contact_id': contact.id, 'contact_name': contact.name}
