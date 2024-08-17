{
    'name': 'Banner Management',
    'version': '1.0',
    'summary': 'A module for managing banners with images and names',
    'sequence': 10,
    'description': """
    A module to manage banners with images, names, and drag-and-drop functionality.
    """,
    'author': 'Your Name',
    'category': 'Website',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/banner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
