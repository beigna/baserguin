# -*- coding: utf-8 -*-

from lib.basic_http import BasicHttp
from lib.constants import STRING, NUMBER, DATETIME_FORMAT


from ConfigParser import ConfigParser
from urllib import urlencode
import yaml
import simplejson
import os
import sys

class EditorMMError(Exception): pass
class FetchingSchedulesError(EditorMMError): pass

class EditorMM(object):
    __slots__ = ('_log', '_schedules_ws', '_extras_ws', '_content_type')

    def __init__(self, logger):
        self._log = logger
        self._content_type = {
            'json': 'application/json',
            'yaml': 'application/yaml',
            'xml': 'application/xml'
        }

    def _parse_config(self, config, section):
        data = {
            'url': config.get(section, 'WsURL'),
            'format': config.get(section, 'WsFormat'),
            'username': config.get(section, 'WsUser'),
            'password': config.get(section, 'WsPass')
        }
        return data

    def load_settings(self):
        """
        Test

        >>> a = EditorMM('logger')
        >>> a.load_settings()
        """

        config = ConfigParser()
        config.read('%s/conf/editormm.conf' % (os.path.abspath(sys.path[0])))

        self._schedules_ws = self._parse_config(config, 'Schedules')
        self._extras_ws = self._parse_config(config, 'Extras')

    def get_extras(self, brand_profile, since, until):
        """
        Test

        >>> a = EditorMM('logger')
        >>> a.load_settings()
        >>> a.get_extras('', '', '')
        """

        between = {'since': since, 'until': until}
        url = '%s?%s' % (self._extras_ws['url'], urlencode(between))

        print url

    def get_schedules(self, brand_profile, since, until):
        """
        Test

        >>> a = EditorMM('logger')
        >>> a.load_settings()
        >>> response = a.get_schedules({'band': '00000004', \
        'partner_id': 4004, 'distribution_channel': 1}, \
        since='2010-07-22 00:00:00', until='2010-07-22 23:00:00')
        Traceback (most recent call last):
        ...
        InvalidResponse: Wanted Status: 200 Response Status: 400

        >>> a = EditorMM('logger')
        >>> a.load_settings()
        >>> response = a.get_schedules({'brand': '00000004', \
        'partner_id': 4004, 'distribution_channel': 1}, \
        since='2010-07-22 00:00:00', until='2010-07-22 23:00:00')
        >>> isinstance(response[0], Schedule)
        True
        """

        try:
            brand_profile['since'] = since
            brand_profile['until'] = until
            brand_profile['is_extra'] = 0

            url = '%s?%s' % (self._schedules_ws['url'], urlencode(brand_profile))

            http = BasicHttp(url)
            http.authenticate(self._schedules_ws['username'],
                self._schedules_ws['password'])

            data = http.request(headers={
                'Accept': self._content_type[self._schedules_ws['format']]}
            )

            yaml_schedules = yaml.load(data['body'])
            schedules = []

            for yaml_schedule in yaml_schedules:
                schedule = Schedule()
                schedule.carrier_id = brand_profile['brand']
                schedule.channel_id = yaml_schedule['channel_id']
                schedule.channel_name = yaml_schedule['channel_name']
                schedule.distribution_channel = \
                    brand_profile['distribution_channel']
                schedule.id = yaml_schedule['id']
                schedule.is_extra = bool(yaml_schedule['is_extra'])
                schedule.package_id = yaml_schedule['package_id']
                schedule.package_name = yaml_schedule['package_name']
                schedule.partner_id = brand_profile['partner_id']

                # TODO modificar algún día el WS para que no lo mande como objeto
                st = yaml_schedule['send_time']
                st = '%02d:%02d:%02d' % (st.hour, st.minute, st.second)
                schedule.send_time = st
                #
                schedule.services = yaml_schedule['services']

                schedules.append(schedule)

            return schedules

        except:
            self._log.exception('Failed while fetching dispatches scheduled.')
            raise FetchingSchedulesError()

class Schedule(object):
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

    def __init__(self, *args, **kwargs):
        self._carrier_id = None
        if kwargs.get('carrier_id'):
            self.carrier_id = kwargs.get('carrier_id')

        self._channel_id = None
        if kwargs.get('channel_id'):
            self.channel_id = kwargs.get('channel_id')

        self._channel_name = None
        if kwargs.get('channel_name'):
            self.channel_name = kwargs.get('channel_name')

        self._distribution_channel = None
        if kwargs.get('distribution_channel'):
            self.distribution_channel = kwargs.get('distribution_channel')

        self._id = None
        if kwargs.get('id'):
            self.id = kwargs.get('id')

        self._is_extra = None
        if kwargs.get('is_extra'):
            self.is_extra = kwargs.get('is_extra')

        self._news_id = None
        if kwargs.get('news_id'):
            self.news_id = kwargs.get('news_id')

        self._package_id = None
        if kwargs.get('package_id'):
            self.packge_id = kwargs.get('package_id')

        self._package_name = None
        if kwargs.get('package_name'):
            self.package_name = kwargs.get('package_name')

        self._partner_id = None
        if kwargs.get('partner_id'):
            self.partner_id = kwargs.get('partner_id')

        self._send_time = None
        if kwargs.get('send_time'):
            self.send_time = kwargs.get('send_time')

        self._services = None
        if kwargs.get('services'):
            self.services = kwargs.get('services')

    def load_yaml(self, data):
        schedules = []

        data = yaml.safe_load(data)

        for schedule in data:
            obj_schedule = Schedule()

            schedules.append()

    # Getters & Setters
    def get_carrier_id(self):
        return self._carrier_id

    def set_carrier_id(self, value):
        if type(value) not in STRING or len(value) != 8 or not value.isdigit():
            raise ValueError('Carrier must be 8 digits string.')
        self._carrier_id = value

    carrier_id = property(get_carrier_id, set_carrier_id)
    ##
    def get_channel_id(self):
        return self._channel_id

    def set_channel_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('channel_id must be positive integer.')
        self._channel_id = value

    channel_id = property(get_channel_id, set_channel_id)
    ##
    def get_channel_name(self):
        return self._channel_name

    def set_channel_name(self, value):
        if type(value) not in STRING:
            raise ValueError('channel_name must be string.')
        self._channel_name = value

    channel_name = property(get_channel_name, set_channel_name)
    ##
    def get_distribution_channel(self):
        return self._distribution_channel

    def set_distribution_channel(self, value):
        if value not in (1, 2, 3, 4, 5):
            raise ValueError('distribution_channel must be 1, 2, 3, 4 or 5.')
        self._distribution_channel = value

    distribution_channel = property(get_distribution_channel,
        set_distribution_channel)
    ##
    def get_id(self):
        return self._id

    def set_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('id must be positive integer.')
        self._id = value

    id = property(get_id, set_id)
    ##
    def get_is_extra(self):
        return self._is_extra

    def set_is_extra(self, value):
        if value not in (0, 1) or type(value) != bool:
            raise ValueError('is_extra must be boolean.')
        self._is_extra = value

    is_extra = property(get_is_extra, set_is_extra)
    ##
    def get_news_id(self):
        return self._news_id

    def set_news_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('news_id must be positive integer.')
        self._news_id = value

    news_id = property(get_news_id, set_news_id)
    ##
    def get_package_id(self):
        return self._package_id

    def set_package_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('package_id must be positive integer.')
        self._package_id = value

    package_id = property(get_package_id, set_package_id)
    ##
    def get_package_name(self):
        return self._package_name

    def set_package_name(self, value):
        if type(value) not in STRING:
            raise ValueError('package_name must be string.')
        self._package_name = value

    package_name = property(get_package_name, set_package_name)
    ##
    def get_partner_id(self):
        return self._partner_id

    def set_partner_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('partner_id must be positive integer.')
        self._partner_id = value

    partner_id = property(get_partner_id, set_partner_id)
    ##
    def get_send_time(self):
        return self._send_time

    def set_send_time(self, value):
        if type(value) not in STRING:
            raise ValueError('send_time must be string.')
        self._send_time = value

    send_time = property(get_send_time, set_send_time)
    ##
    def get_services(self):
        return self._services

    def set_services(self, value):
        if type(value) != list:
            raise ValueError('services must be dict of services.')
        self._services = value

    services = property(get_services, set_services)


