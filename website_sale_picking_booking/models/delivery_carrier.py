# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
import logging
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import timedelta

_logger = logging.getLogger(__name__)
from odoo.addons.resource.models.utils import Intervals

DATETIME_FORMAT = '%d/%m/%Y-%H:%M'
DATE_FORMAT = '%d/%m/%Y'


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    resource_calendar_id = fields.Many2one('resource.calendar', string='Availability')
    available_picking_delay = fields.Float('Hours available for picking the order')
    slot_duration = fields.Float('Duration of picking slot')


    def get_available_slots(self):
        """Return available slots for scheduling collect."""

        start_dt = fields.Datetime.context_timestamp(self, fields.Datetime.now())
        end_dt = fields.Datetime.context_timestamp(self, fields.Datetime.now()) + timedelta(hours=self.available_picking_delay)

        result = {}
        slot_duration = timedelta(hours=self.slot_duration)
        available_interval = self.resource_calendar_id._work_intervals_batch(start_dt, end_dt)

        test_start = False
        for item in available_interval[0]:
            available_start, available_stop = item[0], item[1]
            test_start = available_start
            while test_start and test_start < available_stop:
                test_stop = test_start + slot_duration
                if (
                    test_start >= start_dt
                    and test_start >= available_start
                    and test_stop <= available_stop
                ):
                    if not result.get(test_start.strftime(DATE_FORMAT)):
                        result.setdefault(test_start.strftime(DATE_FORMAT), [])
                    result[test_start.strftime(DATE_FORMAT)].append(test_start.strftime(DATETIME_FORMAT))
                test_start += slot_duration
        return result
    