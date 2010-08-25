# -*- coding: utf-8 -*-

from lib.editormm import Dispatch
from lib.constants import STRING, NUMBER, DATETIME_FORMAT

from uuid import uuid1
import datetime


class SnoopyDispatch(Dispatch):
    __slots__ = (
        '_since',
        '_until',
        '_news_outlet',
        '_uuid',
        '_outlet_file',
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get('schedule'):
            super(SnoopyDispatch, self).__init__(**dict(kwargs.get('schedule')))
        else:
            super(SnoopyDispatch, self).__init__(*args, **kwargs)

        self._since = None
        if kwargs.get('since'):
            self.since = kwargs.get('since')

        self._until = None
        if kwargs.get('until'):
            self.until = kwargs.get('until')

        self._news_outlet = None
        if kwargs.get('news_outlet'):
            # Custom path for some special dispatches.
            self.news_outlet = kwargs.get('news_outlet')

        self._uuid = uuid1().hex

    def from_dict(self, data):
        if not isinstance(data, dict):
            raise TypeError('Argument must be dictonary.')

        self.carrier_id = data['carrier_id']
        self.channel_id = data['channel_id']
        self.channel_name = data['channel_name']
        self.distribution_channel = data['distribution_channel']
        self.id = data['id']
        self.is_extra = data['is_extra']
        if data['news_id']:
            self.news_id = data['news_id']
        self.package_id = data['package_id']
        self.package_name = data['package_name']
        self.partner_id = data['partner_id']
        self.send_time = data['send_time']
        self.services = data['services']
        #
        self.since = datetime.datetime.strptime(data['since'], DATETIME_FORMAT)
        self.until = datetime.datetime.strptime(data['until'], DATETIME_FORMAT)
        if data['news_outlet']:
            self.news_outlet = data['news_outlet']
        if not isinstance(data['uuid'], str) or len(data['uuid']) != 32:
            raise TypeError('UUID must be a valid UUID.')
        self._uuid = data['uuid']

    def as_dict(self):
        data = {
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
            'send_time': self.send_time, # Acts as since when look for news
            'services': self.services,
            #
            'since': None,
            'until': None,
            'news_outlet': self.news_outlet, # Custom path for some
                                             # special dispatches.
            'uuid': self.uuid,
        }

        if not self.is_extra:
            data['until'] = self.until.strftime(DATETIME_FORMAT)
            data['since'] = self.since.strftime(DATETIME_FORMAT)

        return data


    # Getters & Setters
    def get_since(self):
        return self._since

    def set_since(self, value):
        if type(value) != datetime.datetime:
            raise ValueError('since must be datetime.datetime.')
        self._since = value

    since = property(get_since, set_since)
    ##
    def get_until(self):
        return self._until

    def set_until(self, value):
        if type(value) != datetime.datetime:
            raise ValueError('until must be datetime.datetime.')
        self._until = value

    until = property(get_until, set_until)
    ##
    def get_news_outlet(self):
        return self._news_outlet

    def set_news_outlet(self, value):
        if type(value) not in STRING:
            raise ValueError('news_outlet must be string.')
        self._news_outlet = value

    news_outlet = property(get_news_outlet, set_news_outlet)
    ##
    def get_uuid(self):
        return self._uuid

    uuid = property(get_uuid)
    ##
    def get_outlet_file(self):
        return self._outlet_file

    def set_outlet_file(self, value):
        if type(value) not in STRING:
            raise ValueError('outlet_file must be string.')
        self._outlet_file = value

    outlet_file = property(get_outlet_file, set_outlet_file)



'''
scheduled_2010-06-25\ 13\:00\:02_2404.go
-------
carrier_id: '00000004'
channel_id: 112
channel_name: Finanzas Internacionales Argentina
distribution_channel: 1
id: 2404
is_extra: false
news_outlet: null
package_id: 1194
package_name: Finanzas internacionales
partner_id: 4026
send_time: '13:00:00'
services: {id: 218}
since: null
until: '2010-06-25 13:00:00'
uuid: d3abdf5e805911dfb7db0019b9f3422c


extra_2010-06-25\ 13\:00\:02_3074.go
-------
carrier_id: '00000004'
channel_id: 1434
channel_name: Para ratonearse
distribution_channel: 1
id: 3074
is_extra: true
package_id: 1897
package_name: Para ratonearse
partner_id: 4
send_time: null
services: {'id': 873}
since: '2010-06-25 12:58:01'
until: '2010-06-25 13:00:02'
'''

