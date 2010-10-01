# -*- coding: utf-8 -*-

import sys
import os
import unittest
from datetime import datetime, timedelta

from lib.editormm.editormm import EditorMM
from lib.editormm.channel import Channel
from lib.editormm.attachment import Attachment
from lib.editormm.dispatch import Dispatch
from lib.editormm.news import News
from lib.editormm.package import Package
from lib.logger import get_logger
from lib.snoopy_types import SnoopyDispatch


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
        until = since + timedelta(hours=18)

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

    def test_get_channel_ok(self):
        logger = get_logger('EditorMM-Test')
        editormm = EditorMM(logger)
        editormm.load_settings()

        channel = editormm.get_channel(57)

        self.assertEqual(channel.expiration_days, -1)
        self.assertEqual(channel.extra_sm_enabled, False)
        self.assertEqual(channel.extra_sm_length, 0)
        self.assertEqual(channel.name, '9 de Julio')

    def test_get_attachment(self):
        logger = get_logger('EditorMM-Test')
        editormm = EditorMM(logger)
        editormm.load_settings()

        since = datetime(
            datetime.utcnow().year,
            datetime.utcnow().month,
            datetime.utcnow().day,
            11, 27, 30)
        until = since + timedelta(minutes=5)
        brand_profile = {'brand': '00000004', 'partner_id': 4005,
            'distribution_channel': 3}

        dispatches = editormm.get_schedules(brand_profile, since, until)

        for dispatch in dispatches:
            if dispatch.id == 2645:
                schedule_dispatch = SnoopyDispatch(schedule=dispatch.as_dict())
                schedule_dispatch.since = since
                schedule_dispatch.until = until

                break

        news = editormm.get_news(schedule_dispatch)

        self.assertEqual(type(news.attachments[0]), Attachment)

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

    def test_dispatch_ok(self):
        a = Dispatch(
            carrier_id='00000008',
            channel_id=54,
            channel_name='Canal de prueba',
            distribution_channel=1,
            id=132,
            is_extra=True,
            news_id=123,
            package_id=234,
            package_name='Canal de prueba',
            partner_id=4008,
            send_time='2010-08-08 12:22:30',
            services=[{'id': 123}]
        )

        self.assertEqual(a.carrier_id, '00000008')
        self.assertEqual(a.channel_id, 54)
        self.assertEqual(a.channel_name, 'Canal de prueba')
        self.assertEqual(a.distribution_channel, 1)
        self.assertEqual(a.id, 132)
        self.assertEqual(a.is_extra, True)
        self.assertEqual(a.news_id, 123)
        self.assertEqual(a.package_id, 234)
        self.assertEqual(a.package_name, 'Canal de prueba')
        self.assertEqual(a.partner_id, 4008)
        self.assertEqual(str(a.send_time), '2010-08-08 12:22:30')
        self.assertEqual(a.services, [{'id': 123}])

    def test_news_ok(self):
        data = {
    'enhanced_message': 'MSN Mapas Zona Oeste:\nAu. del Oeste: Demora 5 min\nAv. Lope de Vega: Normal\nCamino del Buen Ayre: Normal\nAv. Francisco Beiro: Normal\nPte. La Noria: Normal\nAu. Perito Moreno: Normal\nAv. Rivadavia: Normal\nAv. Juan B. Justo: Normal\n',
    'enhanced_title': 'MSN Mapas Zona Oeste',
    'id': 752980,
    'is_extra': 0,
    'publish_at': '2010-08-31 18:14:30',
    'short_message': 'MSN Mapas Zona Oeste:\nAu. del Oeste: Demora 5 min\nAu. Perito Moreno: Normal\n',
    'short_title': '',
    'title': 'MSN Mapas Zona Oeste',
    'wap_push_title': '',
    'wap_push_url': ''}

        a = News(**dict(data))

        self.assertEqual(a.id, 752980)
        self.assertEqual(a.enhanced_message, data['enhanced_message'])
        self.assertEqual(a.enhanced_title, data['enhanced_title'])
        self.assertEqual(a.is_extra, data['is_extra'])
        self.assertEqual(str(a.publish_at), data['publish_at'])
        self.assertEqual(a.short_message, data['short_message'])
        self.assertEqual(a.short_title, data['short_title'])
        self.assertEqual(a.title, data['title'])
        self.assertEqual(a.wap_push_title, data['wap_push_title'])
        self.assertEqual(a.wap_push_url, data['wap_push_url'])

    def test_package_ok(self):
        data = {
            'channels': [{'id': 168, 'name': 'Policiales Argentina'}],
            'cross_selling': 'test',
            'default_smil': 2,
            'description': 'test',
            'distribution_channel_id': 3,
            'has_fixed_image': 1,
            'id': 540,
            'mms_header': 'test',
            'mms_title': 'Personal News Multimedia',
            'name': 'Policiales Argentina',
            'partner_id': 4005,
            'partner_name': 'Personal MMS'
        }

        a = Package(**dict(data))

    def test_get_package_ok(self):
        logger = get_logger('EditorMM-Test')
        editormm = EditorMM(logger)
        editormm.load_settings()

        dispatch = Dispatch(
            carrier_id='00000008',
            channel_id=54,
            channel_name='Canal de prueba',
            distribution_channel=1,
            id=132,
            is_extra=True,
            news_id=123,
            package_id=540,
            package_name='Canal de prueba',
            partner_id=4008,
            send_time='2010-08-08 12:22:30',
            services=[{'id': 123}]
        )

        package = editormm.get_package(dispatch)

        self.assertEqual(package.id, 540)

if __name__ == '__main__':
    unittest.main()
