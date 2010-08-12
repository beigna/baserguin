# -*- coding: utf-8 -*-

import sys
import os
import shutil
import unittest
from datetime import datetime
from ConfigParser import NoOptionError, NoSectionError

sys.path.append('/home/nachopro/desarrollo/snoopy_oo')
from lib.scheduler import Scheduler
from lib.logger import get_logger

def gen_file(file_path, content):
    open(file_path, 'w').write(content)

class SchedulerTest(unittest.TestCase):
    def setUp(self):
        os.makedirs('/tmp/snoopy_xms/scheduler/')
        os.makedirs('/tmp/snoopy_xms/etc/brands_profiles/')

    def tearDown(self):
        shutil.rmtree('/tmp/snoopy_xms')

    def test_load_settings(self):
        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()

    def test_load_brands_profiles_ok(self):
        gen_file('/tmp/snoopy_xms/etc/brands_profiles/ar_personal.conf', '''[General]
BrandId=00000004

[Sms]
Partners=4,4015,4022,4025,4017,4026,4027,4037,4044

[Mms]
Partners=4017,4005

[Wap]
Partners=4033''')
        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_brands_profiles()

    def test_load_brands_profiles_fail(self):
        gen_file('/tmp/snoopy_xms/etc/brands_profiles/ar_personal.conf', '''[General]
BrandId=00000004

[Sms_cambiado]
Partners=4,4015,4022,4025,4017,4026,4027,4037,4044

[Mms]
Partners=4017,4005

[Wap]
Partners=4033''')
        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        self.assertRaises(NoSectionError, scheduler.load_brands_profiles)

    def test_load_custom_partners_ok(self):
        gen_file('/tmp/snoopy_xms/etc/custom_partners.conf', '''[butterfly]
partners=4024,4037,4038,4039,4046'''),

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_custom_partners()

    def test_load_custom_partners_fail(self):
        gen_file('/tmp/snoopy_xms/etc/custom_partners.conf', '''[butterfly]
partners_mal_escrito=4024'''),

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        self.assertRaises(NoOptionError, scheduler.load_custom_partners)

    def test_load_last_activity_ok(self):
        gen_file('/tmp/snoopy_xms/scheduler/last_activity',
                datetime.utcnow().strftime('%Y-%m-%d 00:00:00'))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_last_activity()

    def test_load_last_activity_fail(self):
        gen_file('/tmp/snoopy_xms/scheduler/last_activity', 'fechaaa 00:00:00')

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        self.assertRaises(ValueError, scheduler.load_last_activity)

    def test_load_history_ok(self):
        gen_file('/tmp/snoopy_xms/scheduler/dispatches_history.cpickle', '''(dp1
L336L
S'2010-08-12'
p2
sL337L
S'2010-08-10'
p3
sL338L
g2
sL67L
S'2010-08-08'
p4
s.''')

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()

    def test_load_history_fail(self):
        gen_file('/tmp/snoopy_xms/scheduler/dispatches_history.cpickle', '''formato invalido''')

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()

if __name__ == '__main__':
    unittest.main()
