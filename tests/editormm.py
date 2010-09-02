# -*- coding: utf-8 -*-

import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.append('/home/nachopro/desarrollo/snoopy_oo')
from lib.editormm.editormm import EditorMM
from lib.editormm.channel import Channel
from lib.editormm.attachment import Attachment
from lib.editormm.dispatch import Dispatch
from lib.editormm.news import News
from lib.editormm.package import Package
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
            send_time='12:22:30',
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
        self.assertEqual(a.send_time, '12:22:30')
        self.assertEqual(a.services, [{'id': 123}])

    def test_news_ok(self):
        data = {'attachments': [
    {'content_type': 'image/jpg','filename': 'map.jpg','id': 3415456},
    {'content_type': 'application/smil','filename': 'cont.smil','id': 3415457},
    {'content_type': 'image/jpg','filename': 'image_0.jpg','id': 3415458},
    {'content_type': 'text/plain','filename': 'text_0.txt','id': 3415459},
    {'content_type': 'image/jpg','filename': 'image_1.jpg','id': 3415460},
    {'content_type': 'text/plain','filename': 'text_1.txt','id': 3415461},
    {'content_type': 'image/jpg','filename': 'image_2.jpg','id': 3415462},
    {'content_type': 'text/plain','filename': 'text_2.txt','id': 3415463},
    {'content_type': 'image/jpg','filename': 'image_3.jpg','id': 3415464},
    {'content_type': 'text/plain','filename': 'text_3.txt','id': 3415465},
    {'content_type': 'image/jpg','filename': 'image_4.jpg','id': 3415466},
    {'content_type': 'text/plain','filename': 'text_4.txt','id': 3415467}],
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
        data = {}

        a = Package(**dict(data))

if __name__ == '__main__':
    unittest.main()
