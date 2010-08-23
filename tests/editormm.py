# -*- coding: utf-8 -*-

import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.append('/home/nachopro/desarrollo/snoopy_oo')
from lib.editormm import EditorMM
from lib.logger import get_logger


class EditorMMTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_settings_ok(self):
        logger = get_logger('EditorMM-Test')
        editormm = EditorMM(logger)
        editormm.load_settings()

    def test_get_extras_ok(self):
        logger = get_logger('EditorMM-Test')
        editormm = EditorMM(logger)
        editormm.load_settings()

        since = datetime(
            datetime.utcnow().year,
            datetime.utcnow().month,
            datetime.utcnow().day
        )
        until = since + timedelta(hours=5)

        dispatches = editormm.get_extras(since, until)
        self.assertEqual(dispatches[0].is_extra, True)

    def test_get_schedules_ok(self):
        logger = get_logger('EditorMM-Test')
        editormm = EditorMM(logger)
        editormm.load_settings()

        since = datetime(
            datetime.utcnow().year,
            datetime.utcnow().month,
            datetime.utcnow().day
        )
        until = since + timedelta(hours=23)
        brand_profile = {'brand': '00000004', 'partner_id': 4004,
            'distribution_channel': 1}

        dispatches = editormm.get_schedules(brand_profile, since, until)
        self.assertEqual(dispatches[0].is_extra, False)

if __name__ == '__main__':
    unittest.main()
