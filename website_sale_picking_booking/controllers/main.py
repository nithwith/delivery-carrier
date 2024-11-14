# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _
from odoo.http import request
from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

DATETIME_FORMAT = '%d/%m/%Y-%H:%M'
    
def _ckeck_strftime_format(value):
    try:
        datetime.strptime(value, DATETIME_FORMAT)
    except ValueError:
        return False
    return True
class WebsiteSaleDelivery(WebsiteSale):
    @http.route(['/shop/update_shipping_slot'], type='json', auth='public', methods=['POST'], website=True)
    def update_eshop_carrier(self, **post):
        order = request.website.sale_get_order()
        if "commitment_date" in post and _ckeck_strftime_format(post['commitment_date']):
            commitment_date = datetime.strptime(post['commitment_date'], DATETIME_FORMAT)
            _logger.info(commitment_date)
            if bool(commitment_date):
                order.commitment_date = commitment_date 


    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)
        if 'deliveries' in values:
            for carrier_id in values['deliveries']:
                if carrier_id.resource_calendar_id:
                    values['available_slots'] = {carrier_id.id : carrier_id.get_available_slots()}
        return values
    

