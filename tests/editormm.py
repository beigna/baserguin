# -*- coding: utf-8 -*-

import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.append('/home/nachopro/desarrollo/snoopy_oo')
from lib.editormm.editormm import EditorMM
from lib.editormm.channel import Channel
from lib.editormm.attachment import Attachment
from lib.logger import get_logger


class EditorMMTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

 #   def test_load_settings_ok(self):
 #       logger = get_logger('EditorMM-Test')
 #       editormm = EditorMM(logger)
 #       editormm.load_settings()

 #   def test_get_extras_ok(self):
 #       logger = get_logger('EditorMM-Test')
 #       editormm = EditorMM(logger)
 #       editormm.load_settings()

 #       since = datetime(
 #           datetime.utcnow().year,
 #           datetime.utcnow().month,
 #           datetime.utcnow().day
 #       )
 #       until = since + timedelta(hours=18)

 #       dispatches = editormm.get_extras(since, until)
 #       self.assertEqual(dispatches[0].is_extra, True)

 #   def test_get_schedules_ok(self):
 #       logger = get_logger('EditorMM-Test')
 #       editormm = EditorMM(logger)
 #       editormm.load_settings()

 #       since = datetime(
 #           datetime.utcnow().year,
 #           datetime.utcnow().month,
 #           datetime.utcnow().day
 #       )
 #       until = since + timedelta(hours=23)
 #       brand_profile = {'brand': '00000004', 'partner_id': 4004,
 #           'distribution_channel': 1}

 #       dispatches = editormm.get_schedules(brand_profile, since, until)
 #       self.assertEqual(dispatches[0].is_extra, False)

    def test_get_channel_ok(self):
        logger = get_logger('EditorMM-Test')
        editormm = EditorMM(logger)
        editormm.load_settings()

        channel = editormm.get_channel(57)

        self.assertEqual(channel.expiration_days, -1)
        self.assertEqual(channel.extra_sm_enabled, False)
        self.assertEqual(channel.extra_sm_length, 0)
        self.assertEqual(channel.name, '9 de Julio')

    def test_channel(self):
        a = Channel(
            expiration_days=-1,
            extra_sm_enabled=0,
            extra_sm_length=0,
            id=57,
            is_autoload=1,
            name='9 de Julio',
            scheduled_sm_enabled=0,
            scheduled_sm_length=0
        )

        self.assertEqual(a.expiration_days, -1)
        self.assertEqual(a.extra_sm_enabled, False)
        self.assertEqual(a.extra_sm_length, 0)
        self.assertEqual(a.id, 57)
        self.assertEqual(a.is_autoload, True)
        self.assertEqual(a.name, '9 de Julio')
        self.assertEqual(a.scheduled_sm_enabled, False)
        self.assertEqual(a.scheduled_sm_length, 0)

    def test_attachment_ok(self):
        a = Attachment(
            id=1,
            filename='test.txt',
            content_type='text/plain',
            content='hola mundo'
        )

        self.assertEqual(a.id, 1)
        self.assertEqual(a.filename, 'test.txt')
        self.assertEqual(a.content_type, 'text/plain')
        self.assertEqual(a.content, 'hola mundo')

    def test_attachment_fail(self):
        try:
            a = Attachment(
                id=1,
                filename='test.txt',
                content_type='text/plain',
            )
        except Exception, e:
            self.assertEqual(type(e), ValueError)


if __name__ == '__main__':
    unittest.main()
