from odoo import http # type: ignore
from odoo.http import request # type: ignore
import json

class ProductController(http.Controller):
    @http.route('/api/products', type='http', auth='public', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):
        products = request.env['product.product'].sudo().search([])
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for product in products:
            product.image_url = f"{base_url}/api/product/{product.id}/image"
            product.url = f"{base_url}/shop/{product.default_code}-{product.id}"
            product.category = product.categ_id.name if product.categ_id else "No Category"
        return request.make_response(json.dumps(products), headers={'Content-Type': 'application/json'})
    
    @http.route('/api/products/by_category', type='http', auth='public', methods=['GET'], csrf=False)
    def get_products_by_category(self, **kwargs):
        category_name = kwargs.get('category')
        if not category_name:
            return request.make_response(json.dumps({'error': 'Category not specified'}), headers={'Content-Type': 'application/json'})
        category = request.env['product.category'].sudo().search([('name', '=', category_name)], limit=1)
        if not category:
            return request.make_response(json.dumps({'error': 'Category not found'}), headers={'Content-Type': 'application/json'})
        
        # Search for products by category, including variants
        products = request.env['product.product'].sudo().search([('categ_id', 'child_of', category.id)])
        
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        messages = []
        elements = []

        for index, product in enumerate(products):
            image_url = f"{base_url}/api/product/{product.id}/image"
            product_url = f"{base_url}/shop/{product.default_code}-{product.id}"
            variant_cost = product.lst_price - product.product_tmpl_id.list_price
            subtitle = f"{product.name} - ({category.name})"
            elements.append({
                'title': f"{int(product.list_price) + int(variant_cost)} دينار",
                'subtitle': subtitle,
                'image_url': image_url,
                'action_url': product_url,
                'buttons': []
            })
            # If we have collected 10 elements, start a new message
            if (index + 1) % 10 == 0:
                messages.append({
                    "type": "cards",
                    "elements": elements,
                    "image_aspect_ratio": "horizontal"
                })
                elements = []

        # Add any remaining elements as the last message
        if elements:
            messages.append({
                "type": "cards",
                "elements": elements,
                "image_aspect_ratio": "horizontal"
            })

        response = {
            "version": "v2",
            "content": {
                "messages": messages,
                "actions": [],
                "quick_replies": []
            }
        }
        return request.make_response(json.dumps(response), headers={'Content-Type': 'application/json'})
