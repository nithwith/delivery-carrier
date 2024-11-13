/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { renderToElement } from "@web/core/utils/render";
import { KeepLast } from "@web/core/utils/concurrency";
import { Component } from "@odoo/owl";

publicWidget.registry.websiteSaleDelivery = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'click .o_delivery_date_select': '_onDeliveryDateClick',
    },

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
    },


    _onDeliveryDateClick: async function (ev) {
        const select = document.querySelector('.o_delivery_date_select')
        const commitment_date = select.options[select.selectedIndex].value
        console.log(commitment_date)

        const result = await this.rpc('/shop/update_shipping_slot', {
            'commitment_date': commitment_date,
        })
    },
});
