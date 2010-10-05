# -*- coding: utf-8 -*-

from lib.constants import DATETIME_FORMAT
from lib.editormm.dispatch import Dispatch
from lib.editormm.channel import Channel
from lib.editormm.news import News
from lib.editormm.attachment import Attachment
from lib.editormm.package import Package


from basic_http import BasicHttp
from ConfigParser import ConfigParser
from urllib import urlencode
from datetime import datetime
import yaml
import simplejson
import os
import sys


class EditorMMError(Exception): pass
class FetchingDispatchesError(EditorMMError): pass

class EditorMM(object):
    __slots__ = (
        '_log',
        '_schedules_ws',
        '_extras_ws',
        '_content_type',
        '_channels_ws',
        '_news_ws',
        '_attachments_ws',
        '_packages_ws',
    )

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
            self._news_ws = self._parse_config(config, 'News')
            self._attachments_ws = self._parse_config(config, 'Attachments')
            self._packages_ws = self._parse_config(config, 'Packages')

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
                url = '%s/?%s' % (ws_data['url'], urlencode(between))

                self._log.debug('Extra URL: %s' % (url))

            else:
                ws_data = self._schedules_ws
                brand_profile['since'] = since.strftime(DATETIME_FORMAT)
                brand_profile['until'] = until.strftime(DATETIME_FORMAT)
                brand_profile['is_extra'] = 0
                url = '%s/?%s' % (ws_data['url'], urlencode(brand_profile))

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
                if is_extra:
                    carrier_id = dispatch_data['brand']
                    distribution_channel = dispatch_data['distribution_channel']
                    partner_id = dispatch_data['partner_id']
                    news_id = dispatch_data['news_id']
                    send_time = '1900-01-01 00:00:00'

                else:
                    carrier_id = brand_profile['brand']
                    distribution_channel=brand_profile['distribution_channel']
                    partner_id = brand_profile['partner_id']

                    # TODO modificar algún día el WS para que
                    # no lo mande como objeto
                    st = dispatch_data['send_time']
                    st = datetime(until.year, until.month, until.day,
                        st.hour, st.minute, st.second)
                    # Exclusivo
                    send_time = st
                    news_id = 0

                dispatch = Dispatch(
                    channel_id=dispatch_data['channel_id'],
                    channel_name=dispatch_data['channel_name'],
                    is_extra=is_extra,
                    id=dispatch_data['id'],
                    package_id=dispatch_data['package_id'],
                    package_name=dispatch_data['package_name'],
                    services=dispatch_data['services'],
                    carrier_id=carrier_id,
                    distribution_channel=distribution_channel,
                    partner_id=partner_id,
                    news_id=news_id,
                    send_time=send_time
                )



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

    def get_package(self, dispatch):
        try:
            ws_data = self._packages_ws
            url = '%s/%d/' % (ws_data['url'], dispatch.package_id)

            self._log.debug('Package URL: %s' % (url))

            http = BasicHttp(url)
            http.authenticate(ws_data['username'], ws_data['password'])

            data = http.GET(headers={
                'Accept': self._content_type[ws_data['format']]}
            )

            package_data = simplejson.loads(data['body'])
            package = Package(**dict(package_data))

            return package

        except Exception, e:
            self._log.exception('Related URL %s' % (url))

    def _get_news_attachment(self, attachment):
        try:
            ws_data = self._attachments_ws
            url = '%s/%d/' % (ws_data['url'], attachment['id'])

            self._log.debug('Attachment URL: %s' % (url))

            http = BasicHttp(url)
            http.authenticate(ws_data['username'], ws_data['password'])

            data = http.GET()

            return Attachment(
                id=attachment['id'],
                filename=attachment['filename'],
                content_type=data['header']['Content-Type'],
                content=data['body']
            )

        except Exception, e:
            self._log.exception('Related URL %s' % (url))
            raise e

    def _get_news_attachments(self, news_dict):
        attachments = []

        for attachment in news_dict['attachments']:
            attachments.append(self._get_news_attachment(attachment))

        return attachments

    def _get_news(self, dispatch):
        ws_data = self._news_ws

        if dispatch.is_extra:
            url = '%s/%d/' % (ws_data['url'], dispatch.news_id)

        else:
            params = urlencode({
                'channel_id': dispatch.channel_id,
                'until': dispatch.send_time
            })
            url = '%s/?%s' % (ws_data['url'], params)

        self._log.debug('News URL: %s' % (url))

        http = BasicHttp(url)
        http.authenticate(ws_data['username'], ws_data['password'])

        data = http.GET(
            headers={'Accept': 'application/json, application/yaml'},
            wanted_status=[200,]
        )

        if data['header']['Content-Type'] == 'application/json':
            news_dict = simplejson.loads(data['body'])

        elif data['header']['Content-Type'] == 'application/yaml':
            news_dict = yaml.load(data['body'])

        if len(news_dict) != 1:
            return None

        news = News(**dict(news_dict[0]))

        if dispatch.distribution_channel == 3:
            news.attachments = self._get_news_attachments(news_dict[0])

        return news

    def get_news(self, dispatch):
        return self._get_news(dispatch)

