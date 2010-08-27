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
class FetchingDispatchesError(EditorMMError): pass

class EditorMM(object):
    __slots__ = ('_log', '_schedules_ws', '_extras_ws', '_content_type',
        '_channels_ws')

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
        try:
            file_path = '%s/conf/editormm.conf' % (
                os.path.abspath(sys.path[0]))

            if not os.path.exists(file_path):
                raise IOError('%s do not exists.' % (file_path))

            config = ConfigParser()
            config.read(file_path)

            self._schedules_ws = self._parse_config(config, 'Schedules')
            self._extras_ws = self._parse_config(config, 'Extras')
            self._channels_ws = self._parse_config(config, 'Channels')

        except Exception, e:
            self._log.exception('Error load settings.')
            raise e

    def _get_dispatches(self, brand_profile, since, until, is_extra):
        try:
            if is_extra:
                ws_data = self._extras_ws
                between = {
                    'since': since.strftime(DATETIME_FORMAT),
                    'until': until.strftime(DATETIME_FORMAT)
                }
                url = '%s?%s' % (ws_data['url'], urlencode(between))

                self._log.debug('Extra URL: %s' % (url))

            else:
                ws_data = self._schedules_ws
                brand_profile['since'] = since.strftime(DATETIME_FORMAT)
                brand_profile['until'] = until.strftime(DATETIME_FORMAT)
                brand_profile['is_extra'] = 0
                url = '%s?%s' % (ws_data['url'], urlencode(brand_profile))

                self._log.debug('Schedule URL: %s' % (url))

            http = BasicHttp(url)
            http.authenticate(ws_data['username'], ws_data['password'])

            data = http.request(headers={
                'Accept': self._content_type[ws_data['format']]}
            )

            if ws_data['format'] == 'yaml':
                dispatches_data = yaml.load(data['body'])

            elif ws_data['format'] == 'json':
                dispatches_data = simplejson.loads(data['body'])

            dispatches_list = []

            for dispatch_data in dispatches_data:
                dispatch = Dispatch()
                dispatch.channel_id = dispatch_data['channel_id']
                dispatch.channel_name = dispatch_data['channel_name']
                dispatch.is_extra = is_extra
                dispatch.id = dispatch_data['id']
                dispatch.package_id = dispatch_data['package_id']
                dispatch.package_name = dispatch_data['package_name']
                dispatch.services = dispatch_data['services']

                if is_extra:
                    dispatch.carrier_id = dispatch_data['brand']
                    dispatch.distribution_channel = \
                        dispatch_data['distribution_channel']
                    dispatch.partner_id = dispatch_data['partner_id']
                    # Exclusivo
                    dispatch.news_id = dispatch_data['news_id']

                else:
                    dispatch.carrier_id = brand_profile['brand']
                    dispatch.distribution_channel = \
                        brand_profile['distribution_channel']
                    dispatch.partner_id = brand_profile['partner_id']

                    # TODO modificar algún día el WS para que
                    # no lo mande como objeto
                    st = dispatch_data['send_time']
                    st = '%02d:%02d:%02d' % (st.hour, st.minute, st.second)
                    # Exclusivo
                    dispatch.send_time = st

                dispatches_list.append(dispatch)

            return dispatches_list

        except Exception, e:
            self._log.exception('Related URL %s' % (url))
            raise e

    def get_extras(self, since, until):
        return self._get_dispatches(None, since, until, is_extra=True)

    def get_schedules(self, brand_profile, since, until):
        return self._get_dispatches(brand_profile, since, until,
            is_extra=False)

    def get_channel(self, id):
        try:
            ws_data = self._channels_ws
            url = '%s/%d/' % (ws_data['url'], id)

            self._log.debug('Channel URL: %s' % (url))

            http = BasicHttp(url)
            http.authenticate(ws_data['username'], ws_data['password'])

            data = http.request(headers={
                'Accept': self._content_type[ws_data['format']]}
            )

            channel_data = simplejson.loads(data['body'])
            channel = Channel(**dict(channel_data))

            return channel

        except Exception, e:
            self._log.exception('Related URL %s' % (url))
            raise e

    def get_channel(self, id):
        try:
            ws_data = self._channels_ws
            url = '%s/%d/' % (ws_data['url'], id)

            self._log.debug('Channel URL: %s' % (url))

            http = BasicHttp(url)
            http.authenticate(ws_data['username'], ws_data['password'])

            data = http.request(headers={
                'Accept': self._content_type[ws_data['format']]}
            )

            channel_data = simplejson.loads(data['body'])
            channel = Channel(**dict(channel_data))

            return channel

        except Exception, e:
            self._log.exception('Related URL %s' % (url))
            raise e

    def get_package(self, package):
        pass

    def _get_news_attachments(self):
        pass

    def _get_news(self):
        pass

    def get_news(self, dispatch):
        if dispatch.is_extra:
            news = self._get_news('/news/123/')

        else:
            news = self._get_news('/news/?channel_id=1&since=2010&until=2011')

        if dispatch.distribution_channel == 3: # MMS
            news.attachments = self._get_news_attachments(news)

        # continuar



class News(object):
    __slots__ = (
        '_attachments'
        '_enhanced_message'
        '_enhanced_title'
        '_id'
        '_is_extra'
        '_publish_at'
        '_short_message'
        '_short_title'
        '_title'
        '_wap_push_title'
        '_wap_push_url'
    )

    def get_is_extra(self):
        return self._is_extra

    def set_is_extra(self, value):
        if type(value) :
            raise ValueError('is_extra must be positive integer.')
        self._is_extra = value

    is_extra = property(get_is_extra, set_is_extra)
    #
    def get_id(self):
        return self._id

    def set_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('id must be positive integer.')
        self._id = value

    id = property(get_id, set_id)
    #
    def get_enhanced_title(self):
        return self._enhanced_title

    def set_enhanced_title(self, value):
        if type(value):
            raise ValueError('enhanced_title must be string.')
        self._enhanced_title = value

    enhanced_title = property(get_enhanced_title, set_enhanced_title)
    #
    def get_enhanced_message(self):
        return self._enhanced_message

    def set_enhanced_message(self, value):
        if type(value) not in STRING:
            raise ValueError('enhanced_message must be string.')
        self._enhanced_message = value

    enhanced_message = property(get_enhanced_message, set_enhanced_message)
    #
    def __str__(self):
        return 'News ID# %d %s' % (self.id, self.short_title or
            self.enhanced_title or self.wap_push_title)

    def get_attachments(self):
        return self._attachments

    def set_attachments(self, value):
        if not value:
            raise ValueError('attachments must be positive integer.')
        self._attachments = value

    attachments = property(get_attachments, set_attachments)
    #

class Package(object):
     'mms_title': 'Personal News Multimedia',
 'name': 'Policiales Argentina',
 'partner_id': 4005,
 'partner_name': 'Personal MMS'
 channels': [{'id': 168, 'name': 'Policiales Argentina'}],
 'cross_selling': '',
 'default_smil': 2,
 'description': '',
 'distribution_channel_id': 3,
 'has_fixed_image': 1,
 'id': 540,
 'mms_header':'

class Attachment(object):
    __slots__ = (
        '_id',
        '_filename',
        '_content_type',
        '_content'
    )

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.filename = kwargs.get('filename')
        self.content_type = kwargs.get('content_type')
        self.content = kwargs.get('content')

    def __str__(self):
        return '%s %s' % (self.filename, self.content_type)
    #
    def get_content(self):
        return self._content

    def set_content(self, value):
        if type(value) not in STRING:
            raise ValueError('content must be string.')
        self._content = value

    content = property(get_content, set_content)
    #
    def get_content_type(self):
        return self._content_type

    def set_content_type(self, value):
        if type(value) not in STRING:
            raise ValueError('content_type must be string.')
        self._content_type = value

    content_type = property(get_content_type, set_content_type)
    #
    def get_filename(self):
        return self._filename

    def set_filename(self, value):
        if type(value) not in STRING:
            raise ValueError('filename must be string.')
        self._filename = value

    filename = property(get_filename, set_filename)
    #
    def get_id(self):
        return self._id

    def set_id(self, value):
        if type(value) not in NUMBER or value < 0:
            raise ValueError('id must be positive integer.')
        self._id = value

    id = property(get_id, set_id)
    #

class Channel(object):
    __slots__ = (
        '_expiration_days',
        '_extra_sm_enabled',
        '_extra_sm_length',
        '_id',
        '_is_autoload',
        '_name',
        '_scheduled_sm_enabled',
        '_scheduled_sm_length'
    )

    def __unicode__(self):
        return u'ID# %d %s' % (self.id, self.name)

    def __str__(self):
        return 'ID# %d %s' % (self.id, self.name.encode('utf-8'))

    def __init__(self, *args, **kwargs):
        self._expiration_days = None
        if kwargs.get('expiration_days'):
            self.expiration_days = kwargs.get('expiration_days')

        self._extra_sm_enabled = False
        if kwargs.get('extra_sm_enabled'):
            self.extra_sm_enabled = kwargs.get('extra_sm_enabled')

        self._extra_sm_length = 0
        if kwargs.get('extra_sm_length'):
            self.extra_sm_length = kwargs.get('extra_sm_length')

        self._id = None
        if kwargs.get('id'):
            self.id = kwargs.get('id')

        self._is_autoload = False
        if kwargs.get('is_autoload'):
            self.is_autoload = kwargs.get('is_autoload')

        self._name = None
        if kwargs.get('name'):
            self.name = kwargs.get('name')

        self._scheduled_sm_enabled = False
        if kwargs.get('scheduled_sm_enabled'):
            self.scheduled_sm_enabled = kwargs.get('scheduled_sm_enabled')

        self._scheduled_sm_length = 0
        if kwargs.get('scheduled_sm_length'):
            self.scheduled_sm_length = kwargs.get('scheduled_sm_length')


    def get_scheduled_sm_length(self):
        return self._scheduled_sm_length

    def set_scheduled_sm_length(self, value):
        if type(value) not in NUMBER or value < 0:
            raise ValueError('scheduled_sm_length must be positive integer.')
        self._scheduled_sm_length = value

    scheduled_sm_length = property(get_scheduled_sm_length,
        set_scheduled_sm_length)
    #
    def get_scheduled_sm_enabled(self):
        return self._scheduled_sm_enabled

    def set_scheduled_sm_enabled(self, value):
        if value not in (0, 1) or type(value) != bool:
            raise ValueError('scheduled_sm_enabled must be boolean.')
        self._scheduled_sm_enabled = bool(value)

    scheduled_sm_enabled = property(get_scheduled_sm_enabled,
        set_scheduled_sm_enabled)
    #
    def get_name(self):
        return self._name

    def set_name(self, value):
        if type(value) not in STRING:
            raise ValueError('name must be string.')
        self._name = value

    name = property(get_name, set_name)
    #
    def get_is_autoload(self):
        return self._is_autoload

    def set_is_autoload(self, value):
        if value in (0, 1) or type(value) == bool:
            self._is_autoload = bool(value)
        else:
            raise ValueError('is_autoload must be boolean.')

    is_autoload = property(get_is_autoload, set_is_autoload)
    #
    def get_id(self):
        return self._id

    def set_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('id must be positive integer.')
        self._id = value

    id = property(get_id, set_id)
    #
    def get_extra_sm_length(self):
        return self._extra_sm_length

    def set_extra_sm_length(self, value):
        if type(value) not in NUMBER or value < 0:
            raise ValueError('extra_sm_length must be positive integer.')
        self._extra_sm_length = value

    extra_sm_length = property(get_extra_sm_length, set_extra_sm_length)
    #
    def get_extra_sm_enabled(self):
        return self._extra_sm_enabled

    def set_extra_sm_enabled(self, value):
        if value not in (0, 1) or type(value) != bool:
            raise ValueError('extra_sm_enabled must be boolean.')
        self._extra_sm_enabled = bool(value)

    extra_sm_enabled = property(get_extra_sm_enabled, set_extra_sm_enabled)
    #
    def get_expiration_days(self):
        return self._expiration_days

    def set_expiration_days(self, value):
        if type(value) not in NUMBER:
            raise ValueError('expiration_days must be positive integer.')
        self._expiration_days = value

    expiration_days = property(get_expiration_days, set_expiration_days)


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

    def __unicode__(self):
        value = u'ID# %d %s - %s' % (self.id, self.package_name,
            self.channel_name)

        if self.is_extra:
            value = '%s News ID# %d' % (value, self.news_id)

        return value

    def __str__(self):
        value = 'ID# %d %s - %s' % (self.id,
            self.package_name.encode('utf-8'),
            self.channel_name.encode('utf-8'))

        if self.is_extra:
            value = '%s News ID# %d' % (value, self.news_id)

        return value

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

        self._is_extra = False
        if kwargs.get('is_extra'):
            self.is_extra = kwargs.get('is_extra')

        self._news_id = None
        if kwargs.get('news_id'):
            self.news_id = kwargs.get('news_id')

        self._package_id = None
        if kwargs.get('package_id'):
            self.package_id = kwargs.get('package_id')

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
        pass

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

        if isinstance(value, str):
            value = value.decode('utf-8')

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
        self._is_extra = bool(value)

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

        if isinstance(value, str):
            value = value.decode('utf-8')

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


