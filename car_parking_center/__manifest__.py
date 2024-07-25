
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
        'web',
        'board',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/parking_center_menus.xml',
        'views/parking_center_car_views.xml',
        'views/parking_center_visit_views.xml',
        'views/parking_center_payment_views.xml',
        'views/parking_center_dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'car_parking_center/static/src/components/parking_center_dashboard.js',
            'car_parking_center/static/src/components/parking_center_dashboard.xml',
        ]
    },
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
}
