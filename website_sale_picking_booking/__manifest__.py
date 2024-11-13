# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Click and collect disponibility',
    'version': '1.0',
    'category': 'Website/Website',
    'description': """

""",
    'depends': ['website_sale_picking',],
    'data': [
        'views/templates.xml',
        'views/delivery_view.xml'
    ],
    'demo': [
    ],    
    'assets': {
        'web.assets_frontend': [
            'website_sale_picking_booking/static/src/js/website_sale_delivery.js',
        ],
    },
    'license': 'LGPL-3',
}
