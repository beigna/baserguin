# -*- coding: utf-8 -*-

from lib.basic_http import BasicHttp
from lib.constants import DATETIME_FORMAT
from lib.editormm.dispatch import Dispatch
from lib.editormm.channel import Channel


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

            data = http.GET(headers={
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

            data = http.GET(headers={
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



class dNews(object):
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


class dPackage(object):
     #'channels': [{'id': 168, 'name': 'Policiales Argentina'}],
     #'cross_selling': '',
     #'default_smil': 2,
     #'description': '',
     #'distribution_channel_id': 3,
     #'has_fixed_image': 1,
     #'id': 540,
     #'mms_header':'
     #'mms_title': 'Personal News Multimedia',
     #'name': 'Policiales Argentina',
     #'partner_id': 4005,
     #'partner_name': 'Personal MMS'
     pass


