{
    'name': 'Product Brand with Sequence',
    'version': '1.1',
    'category': 'Product',
    'summary': 'Add brand to products',
    'depends': ['product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'controllers': [
        'controllers/image_controller.py',
    ],
}
