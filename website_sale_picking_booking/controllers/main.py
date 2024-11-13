# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _
from odoo.addons.website_sale.controllers.main import PaymentPortal
from odoo.exceptions import ValidationError
from odoo.http import request


import json
from odoo import http, _
from odoo.http import request
from odoo.addons.payment import utils as payment_utils
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

DATETIME_FORMAT = '%d/%m/%Y-%H:%M'

class WebsiteSaleDelivery(WebsiteSale):

    @http.route(['/shop/update_shipping_slot'], type='json', auth='public', methods=['POST'], website=True)
    def update_eshop_carrier(self, **post):
        order = request.website.sale_get_order()
        commitment_date = datetime.strptime(post['commitment_date'], '%d/%m/%Y-%H:%M')
        if "commitment_date" in post:
            commitment_date = datetime.strptime(post['commitment_date'], DATETIME_FORMAT)
            if bool(commitment_date):
                order.commitment_date = commitment_date 


    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)
        if 'deliveries' in values:
            for carrier_id in values['deliveries']:
                if carrier_id.resource_calendar_id:
                    values['available_slots'] = {carrier_id.id : carrier_id.get_available_slots()}
        return values