# -*- coding: utf-8 -*-
import sys
import os
import shutil
import unittest
import glob
import yaml
from datetime import datetime
from ConfigParser import NoOptionError, NoSectionError

sys.path.append('/home/nachopro/desarrollo/snoopy_oo')

from lib.scheduler import Scheduler
from lib.logger import get_logger
from lib.editormm.dispatch import Dispatch
from lib.snoopy_types import SnoopyDispatch

def gen_file(file_path, content):
    open(file_path, 'w').write(content)


class SchedulerTest(unittest.TestCase):
    def setUp(self):
        os.makedirs('/tmp/snoopy_xms/scheduler/')
        os.makedirs('/tmp/snoopy_xms/etc/brands_profiles/')
        os.makedirs('/tmp/snoopy_xms/reports_pool/')

    def tearDown(self):
        shutil.rmtree('/tmp/snoopy_xms')

    def test_load_settings(self):
        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()

    def test_load_brands_profiles_ok(self):
        gen_file('/tmp/snoopy_xms/etc/brands_profiles/ar_personal.conf',
            """[General]
BrandId=00000004

[Sms]
Partners=4,4015,4022,4025,4017,4026,4027,4037,4044

[Mms]
Partners=4017,4005

[Wap]
Partners=4033""")
        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_brands_profiles()

    def test_load_brands_profiles_fail(self):
        gen_file('/tmp/snoopy_xms/etc/brands_profiles/ar_personal.conf',
            """[General]
BrandId=00000004

[Sms_cambiado]
Partners=4,4015,4022,4025,4017,4026,4027,4037,4044

[Mms]
Partners=4017,4005

[Wap]
Partners=4033""")
        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        self.assertRaises(NoSectionError, scheduler.load_brands_profiles)

    def test_load_custom_partners_ok(self):
        gen_file('/tmp/snoopy_xms/etc/custom_partners.conf',
            """[butterfly]
partners=4024,4037,4038,4039,4046""")

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_custom_partners()

    def test_load_custom_partners_fail(self):
        gen_file('/tmp/snoopy_xms/etc/custom_partners.conf', '''[butterfly]
partners_mal_escrito=4024''')

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
        # TODO: Test dummie, nunca va a fallar. Revisar
        gen_file('/tmp/snoopy_xms/scheduler/dispatches_history.cpickle', '''formato invalido''')

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()

    def test_is_dispatch_in_history_true(self):
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'send_time': '2010-05-05 12:30:00',
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': False,
            'channel_id': 66L
        }
        dispatch = Dispatch(**dict(dispatch_dict))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()
        scheduler.add_dispatch_to_history(dispatch)
        self.assertTrue(scheduler.is_dispatch_in_history(dispatch))

    def test_is_dispatch_in_history_false(self):
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'send_time': '2010-05-05 12:30:00',
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': False,
            'channel_id': 66L
        }
        dispatch = Dispatch(**dict(dispatch_dict))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()
        self.assertFalse(scheduler.is_dispatch_in_history(dispatch))

    def test_is_dispatch_in_history_true_extra(self):
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': True,
            'news_id': 123456,
            'channel_id': 66L
        }
        dispatch = Dispatch(**dict(dispatch_dict))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()
        scheduler.add_dispatch_to_history(dispatch)
        self.assertTrue(scheduler.is_dispatch_in_history(dispatch))

    def test_can_be_send_true(self):
        gen_file('/tmp/snoopy_xms/etc/brands_profiles/ar_personal.conf', '''[General]
BrandId=00000004

[Sms]
Partners=4004,4015,4022,4025,4017,4026,4027,4037,4044

[Mms]
Partners=4017,4005

[Wap]
Partners=4033''')
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': True,
            'news_id': 123456,
            'channel_id': 66L
        }
        dispatch = Dispatch(**dict(dispatch_dict))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_brands_profiles()
        self.assertTrue(scheduler.can_be_send(dispatch))

    def test_can_be_send_false(self):
        gen_file('/tmp/snoopy_xms/etc/brands_profiles/ar_personal.conf', '''[General]
BrandId=00000004

[Sms]
Partners=400,4015,4022,4025,4017,4026,4027,4037,4044

[Mms]
Partners=4017,4005

[Wap]
Partners=4033''')
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': True,
            'news_id': 123456,
            'channel_id': 66L
        }
        dispatch = Dispatch(**dict(dispatch_dict))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_brands_profiles()
        self.assertFalse(scheduler.can_be_send(dispatch))

    def test_save_history_ok(self):
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'send_time': '2010-01-01 12:30:00',
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': False,
            'channel_id': 66L
        }
        dispatch = Dispatch(**dict(dispatch_dict))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()
        scheduler.add_dispatch_to_history(dispatch)
        scheduler.save_history()

        scheduler_bis = Scheduler(logger)
        scheduler_bis.load_settings()
        scheduler_bis.load_history()
        self.assertTrue(scheduler_bis.is_dispatch_in_history(dispatch))

    def test_save_history_fail(self):
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'send_time': '2010-05-05 12:30:00',
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': False,
            'channel_id': 66L
        }
        dispatch = Dispatch(**dict(dispatch_dict))

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_history()
        scheduler.add_dispatch_to_history(dispatch)

        scheduler_bis = Scheduler(logger)
        scheduler_bis.load_settings()
        scheduler_bis.load_history()
        self.assertFalse(scheduler_bis.is_dispatch_in_history(dispatch))

    def test_check_news_outlet_ok(self):
        gen_file('/tmp/snoopy_xms/etc/custom_partners.conf', '''[butterfly]
partners=4024,4037,4038,4039,4046''')

        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'send_time': '2010-09-09 12:30:00',
            'services': [],
            'partner_id': 4046,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': False,
            'channel_id': 66L
        }

        snoopy_dispatch = SnoopyDispatch(schedule=dispatch_dict)

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_custom_partners()
        scheduler.check_news_outlet(snoopy_dispatch)

        self.assertEqual(snoopy_dispatch.news_outlet,
            '/tmp/snoopy_xms/news_butterfly_pool')

    def test_check_news_outlet_fail(self):
        gen_file('/tmp/snoopy_xms/etc/custom_partners.conf', '''[butterfly]
partners=4024,4037,4038,4039,4046''')

        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'send_time': '2010-09-09 12:30:00',
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': False,
            'channel_id': 66L
        }

        snoopy_dispatch = SnoopyDispatch(schedule=dispatch_dict)

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.load_custom_partners()
        scheduler.check_news_outlet(snoopy_dispatch)

        self.assertEqual(snoopy_dispatch.news_outlet, None)

    def test_save_last_activity_ok(self):
        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.save_last_activity()

    def test_report_ok(self):
        dispatch_dict = {
            'package_name': u'Aries',
            'carrier_id': '00000004',
            'package_id': 495L,
            'send_time': '2010-05-06 12:30:00',
            'services': [],
            'partner_id': 4004,
            'id': 546L,
            'distribution_channel': 1,
            'channel_name': u'Aries',
            'is_extra': False,
            'channel_id': 66L
        }
        snoopy_dispatch = SnoopyDispatch(schedule=dispatch_dict)

        logger = get_logger('Scheduler-Test')
        scheduler = Scheduler(logger)
        scheduler.load_settings()
        scheduler.report(snoopy_dispatch)

        files = glob.glob('/tmp/snoopy_xms/reports_pool/sch_*.go')
        data = yaml.safe_load(open(files[0], 'r').read())

        original_data = (snoopy_dispatch.uuid, snoopy_dispatch.partner_id,
            snoopy_dispatch.id, snoopy_dispatch.is_extra,
            snoopy_dispatch.send_time)
        loaded_data = (data['uuid'], data['partner'], data['id'],
            data['is_extra'], data['date'])

        self.assertEqual(original_data, loaded_data)

if __name__ == '__main__':
    unittest.main()
