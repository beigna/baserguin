# -*- coding: utf-8 -*-

from simplejson import dumps

from lib.constants import STRING, NUMBER
from lib.basic_types import Boolean, String, Integer, DateTime


class Dispatch(object):
    __slots__ = (
        '_carrier_id',
        '_channel_id',
        '_channel_name',
        '_distribution_channel',
        '_id',
        '_is_extra',
        '_news_id',
        '_package_id',
        '_package_name',
        '_partner_id',
        '_send_time',
        '_services'
    )

    def as_dict(self):
        return {
            'carrier_id': self.carrier_id,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'distribution_channel': self.distribution_channel,
            'id': self.id,
            'is_extra': self.is_extra,
            'news_id': self.news_id,
            'package_id': self.package_id,
            'package_name': self.package_name,
            'partner_id': self.partner_id,
            'send_time': self.send_time,
            'services': self.services
        }

    def as_json(self):
        return dumps({
            'carrier_id': self.carrier_id,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'distribution_channel': self.distribution_channel,
            'id': self.id,
            'is_extra': self.is_extra,
            'news_id': self.news_id,
            'package_id': self.package_id,
            'package_name': self.package_name,
            'partner_id': self.partner_id,
            'send_time': str(self.send_time),
            'services': self.services
        })

    def __unicode__(self):
        value = u'ID# %d %s - %s' % (self.id, self.package_name,
            self.channel_name)

        if self.is_extra:
            value = '%s News ID# %d' % (value, self.news_id)

        return value

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __init__(self, *args, **kwargs):
        self.carrier_id = kwargs.get('carrier_id')
        self.channel_id = kwargs.get('channel_id')
        self.channel_name = kwargs.get('channel_name')
        self.distribution_channel = kwargs.get('distribution_channel')
        self.id = kwargs.get('id')

        self.is_extra = kwargs.get('is_extra', False)
        self.news_id = kwargs.get('news_id', 0)

        self.package_id = kwargs.get('package_id')
        self.package_name = kwargs.get('package_name')

        self.partner_id = kwargs.get('partner_id')

        self.send_time = kwargs.get('send_time', '1900-01-01 00:00:00')

        self.services = kwargs.get('services')

    # Getters & Setters
    def get_carrier_id(self):
        return self._carrier_id

    def set_carrier_id(self, value):
        if type(value) not in STRING or len(value) != 8 or not value.isdigit():
            raise ValueError('Carrier must be 8 digits string.')
        self._carrier_id = value

    carrier_id = property(get_carrier_id, set_carrier_id)
    #
    def get_channel_id(self):
        return self._channel_id.value
    def set_channel_id(self, value):
        self._channel_id = Integer(value)
    channel_id = property(get_channel_id, set_channel_id)
    #
    def get_channel_name(self):
        return self._channel_name.value
    def set_channel_name(self, value):
        self._channel_name = String(value)
    channel_name = property(get_channel_name, set_channel_name)
    #
    def get_distribution_channel(self):
        return self._distribution_channel

    def set_distribution_channel(self, value):
        if value not in (1, 2, 3, 4, 5):
            raise ValueError('distribution_channel must be 1, 2, 3, 4 or 5.')
        self._distribution_channel = value

    distribution_channel = property(get_distribution_channel,
        set_distribution_channel)
    #
    def get_id(self):
        return self._id.value
    def set_id(self, value):
        self._id = Integer(value)
    id = property(get_id, set_id)
    #
    def get_is_extra(self):
        return self._is_extra.value
    def set_is_extra(self, value):
        self._is_extra = Boolean(value)
    is_extra = property(get_is_extra, set_is_extra)
    #
    def get_news_id(self):
        return self._news_id.value
    def set_news_id(self, value):
        self._news_id = Integer(value)
    news_id = property(get_news_id, set_news_id)
    #
    def get_package_id(self):
        return self._package_id.value
    def set_package_id(self, value):
        self._package_id = Integer(value)
    package_id = property(get_package_id, set_package_id)
    #
    def get_package_name(self):
        return self._package_name.value
    def set_package_name(self, value):
        self._package_name = String(value)
    package_name = property(get_package_name, set_package_name)
    #
    def get_partner_id(self):
        return self._partner_id.value
    def set_partner_id(self, value):
        self._partner_id = Integer(value)
    partner_id = property(get_partner_id, set_partner_id)
    #
    def get_send_time(self):
        return self._send_time.value
    def set_send_time(self, value):
        self._send_time = DateTime(value)
    send_time = property(get_send_time, set_send_time)
    #
    def get_services(self):
        return self._services

    def set_services(self, value):
        if type(value) != list:
            raise ValueError('services must be dict of services.')
        self._services = value

    services = property(get_services, set_services)
    #
