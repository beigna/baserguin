# -*- coding: utf-8 -*-

import sys
import os
import unittest

from lib.newser import Newser
from lib.logger import get_logger

class NewserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_settings(self):
        logger = get_logger('Newser-Test')
        cfg = Newser.load_settings(logger)

        self.assertEqual(cfg['processes'], 2)

if __name__ == '__main__':
    unittest.main()
