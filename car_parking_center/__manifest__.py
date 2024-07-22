
{
    'name': 'Car Parking Center',
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Car Parking Center""",
    'license': 'LGPL-3',
    'author': 'Volodymyr Dziadyk',
    'support': 'dvol@oneservice.in.ua',
    'website': 'https://www.oneservice-consulting.com',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/parking_center_menus.xml',
        'views/parking_center_car_views.xml',
        'views/parking_center_visit_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': False,
    'installable': True,
    'auto_install': False,
}
