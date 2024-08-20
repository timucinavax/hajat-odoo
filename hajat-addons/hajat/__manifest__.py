# __manifest__.py

{
    'name': 'Hajat Custom API',
    'version': '1.2',
    'category': 'Custom',
    'summary': 'Returns products in JSON format, and creates contacts using an API endpoint',
    'description': 'An Odoo module that provides an endpoint to return products in JSON format',
    'author': 'Mohamed Elkmeshi',
    'depends': ['base', 'product','contacts','product_brand_2','website_sale','sale'],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
