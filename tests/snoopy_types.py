# -*- coding: utf-8 -*-

import sys
import os
import unittest
import datetime

sys.path.append('/home/nachopro/desarrollo/snoopy_oo')
from lib.snoopy_types import SnoopyDispatch
from lib.logger import get_logger

class SnoopyDispatchTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_from_dict(self):
        data = {
            'carrier_id': '00000004',
            'channel_id': 305,
            'channel_name': 'Maya Venado',
            'distribution_channel': 1,
            'id': 2680,
            'is_extra': False,
            'news_id': None,
            'news_outlet': None,
            'package_id': 1611,
            'package_name': 'Maya Venado',
            'partner_id': 4,
            'send_time': '14:30:00',
            'services': [{'id': 721}],
            'since': '2010-08-25 00:14:32',
            'until': '2010-08-25 21:02:20',
            'uuid': '195dd360b08c11df909600d0b7884183'
        }
        a = SnoopyDispatch()

        a.from_dict(data)

        self.assertEqual(a.carrier_id, data['carrier_id'])
        self.assertEqual(a.channel_id, data['channel_id'])
        self.assertEqual(a.channel_name, data['channel_name'])
        self.assertEqual(a.distribution_channel, data['distribution_channel'])
        self.assertEqual(a.id, data['id'])
        self.assertEqual(a.is_extra, data['is_extra'])
        self.assertEqual(a.news_id, data['news_id'])
        self.assertEqual(a.news_outlet, data['news_outlet'])
        self.assertEqual(a.package_id, data['package_id'])
        self.assertEqual(a.package_name, data['package_name'])
        self.assertEqual(a.partner_id, data['partner_id'])
        self.assertEqual(a.send_time, data['send_time'])
        self.assertEqual(a.services, data['services'])
        self.assertEqual(a.since, datetime.datetime(2010, 8, 25, 0, 14, 32))
        self.assertEqual(a.until, datetime.datetime(2010, 8, 25, 21, 2, 20))
        self.assertEqual(a.uuid, data['uuid'])


if __name__ == '__main__':
    unittest.main()
