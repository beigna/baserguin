# -*- coding: utf-8 -*-

import cPickle
import glob
import os
import sys

from ConfigParser import ConfigParser
from datetime import datetime
from tempfile import mktemp
import yaml

from lib.constants import DATETIME_FORMAT

class basic_fake_daemon(object):
    __slots__ = ()

    def __init__(self, logger):
        raise NotImplementedError()

    def load_settings(self):
        raise NotImplementedError()


class SchedulerHistoryError(Exception):
    pass


class Scheduler(basic_fake_daemon):
    __slots__ = (
        '_log',
        '_brands_profiles',
        '_custom_partners',
        '_last_activity',
        '_start_time',
        '_history',

        '_pid_path',
        '_last_activity_path',
        '_last_status_path',
        '_dispatches_history_path',
        '_dispatches_outlet_path',
        '_reports_outlet_path',
        '_brands_profiles_path',
        '_custom_partners_path',
        '_basedir'
    )

    def __init__(self, logger):
        self._log = logger
        self._start_time = datetime.utcnow()

    def load_settings(self):  # has test case
        try:
            file_path = '%s/conf/scheduler.conf' % (
                os.path.abspath(sys.path[0]))

            if not os.path.exists(file_path):
                raise IOError('%s do not exists.' % file_path)

            config = ConfigParser()
            config.read(file_path)

            self._pid_path = config.get('General', 'pid')
            self._last_activity_path = config.get('General', 'LastActivity')
            self._last_status_path = config.get('General', 'LastStatus')
            self._dispatches_history_path = \
                config.get('General', 'DispatchesHistory')
            self._dispatches_outlet_path = \
                config.get('General', 'DispatchesOutlet')
            self._reports_outlet_path = config.get('General', 'ReportsOutlet')
            self._brands_profiles_path =\
                config.get('General', 'BrandsProfiles')
            self._custom_partners_path =\
                config.get('General', 'CustomPartners')
            self._basedir = config.get('General', 'BaseDir')

        except Exception, e:
            self._log.exception('Error load settings.')
            raise e

    def load_brands_profiles(self):  # has test case
        try:
            self._brands_profiles = []

            files_to_load = glob.glob('%s/*.conf' % self._brands_profiles_path)

            for file_to_load in files_to_load:
                config = ConfigParser()
                config.read(file_to_load)

                brand_id = config.get('General', 'BrandId')
                partners_sms = config.get('Sms', 'Partners')
                partners_mms = config.get('Mms', 'Partners')
                partners_wap = config.get('Wap', 'Partners')

                for partner in partners_sms.split(','):
                    if partner.isdigit():
                        # 1 = sms distribution_channel
                        self._brands_profiles.append({
                            'brand': brand_id,
                            'partner_id': int(partner),
                            'distribution_channel': 1
                        })

                for partner in partners_mms.split(','):
                    if partner.isdigit():
                        # 3 = mms distribution_channel
                        self._brands_profiles.append({
                            'brand': brand_id,
                            'partner_id': int(partner),
                            'distribution_channel': 3
                        })

                for partner in partners_wap.split(','):
                    if partner.isdigit():
                        # 5 = wap distribution_channel
                        self._brands_profiles.append({
                            'brand': brand_id,
                            'partner_id': int(partner),
                            'distribution_channel': 5
                        })

        except Exception, e:
            self._log.exception('Error load brands profiles.')
            raise e

    def load_custom_partners(self):  # has test case
        try:
            config = ConfigParser()
            config.read('%s/custom_partners.conf' % self._custom_partners_path)

            self._custom_partners = {}

            for section in config.sections():
                partners = config.get(section, 'Partners')
                for partner in partners.split(','):
                    partner = int(partner)
                    self._custom_partners[partner] = section

        except Exception, e:
            self._log.exception('Error load custom partners.')
            raise e

    def check_news_outlet(self, dispatch):  # has test case
        if dispatch.partner_id in self._custom_partners:
            dispatch.news_outlet = '%s/news_%s_pool' % (self._basedir,
                self._custom_partners[dispatch.partner_id])

    def load_last_activity(self):  # has test case
        fp = open(self._last_activity_path, 'r')
        last_activity = fp.read().strip()
        fp.close()
        self._last_activity = datetime.strptime(last_activity, DATETIME_FORMAT)

    def save_last_activity(self):  # has test case
        fp = open(self._last_activity_path, 'w')
        fp.write(self._start_time.strftime(DATETIME_FORMAT))
        fp.close()

    def save_last_status(self, status):
        fp = open(self._last_status_path, 'w')
        fp.write(status)
        fp.close

    def load_history(self):  # has test case
        try:
            fp = open(self._dispatches_history_path, 'r')
            self._history = cPickle.load(fp)
            fp.close()
        except:
            self._log.warning('Creating a new and empty history.')
            self._history = {}

    def can_be_send(self, dispatch):
        result = filter(lambda e: e['brand'] == dispatch.carrier_id
            and e['partner_id'] == dispatch.partner_id
            and e['distribution_channel'] == dispatch.distribution_channel,
            self._brands_profiles)

        if len(result) == 1:
            return True

        return False

    def is_dispatch_in_history(self, dispatch):  # has test case
        if dispatch.is_extra:
            key = '%d-%d' % (dispatch.id, dispatch.news_id)
        else:
            key = dispatch.id

        return self._history.get(key) == \
            self._start_time.strftime('%Y-%m-%d')

    def inject_to_queue(self, dispatch):
        data = dispatch.as_json()

        filename = '%s/dispatchd_%s_%d.tmp' % (self._dispatches_outlet_path,
            self._start_time.strftime(DATETIME_FORMAT.replace(' ', '_')),
            dispatch.id)
        fp = open(filename, 'w')
        fp.write(data)
        fp.close()

        dispatch.outlet_file = filename

    def report(self, dispatch):  # has test case
        data = {
            'uuid': dispatch.uuid,
            'partner': dispatch.partner_id,
            'id': dispatch.id,
            'is_extra': dispatch.is_extra,
            'date': dispatch.send_time,
            'notified_at': datetime.utcnow().strftime(DATETIME_FORMAT)
        }

        filename = mktemp(prefix='sch_', suffix='.tmp',
            dir=self._reports_outlet_path)
        fp = open(filename, 'w')
        fp.write(yaml.safe_dump(data))
        fp.close()

        os.rename(filename, filename.replace('.tmp', '.go'))

    def add_dispatch_to_history(self, dispatch):  # implicit tests
        if dispatch.is_extra:
            key = '%d-%d' % (dispatch.id, dispatch.news_id)
        else:
            key = dispatch.id

        self._history[key] = self._start_time.strftime('%Y-%m-%d')

    def save_history(self):  # has test case
        if not isinstance(self._history, dict):
            raise SchedulerHistoryError('The history is not a dict.')

        try:
            fp = open(self._dispatches_history_path, 'w')
            cPickle.dump(self._history, fp)
            fp.close()

        except Exception, e:
            self._log.exception('Error on save history.')
            raise e

    # Getters & Setters
    def get_pid_path(self):
        return self._pid_path

    def get_brands_profiles(self):
        return self._brands_profiles

    def get_custom_partners(self):
        return self._custom_partners

    def get_last_activity(self):
        return self._last_activity

    def get_start_time(self):
        return self._start_time

    pid_path = property(get_pid_path)
    brands_profiles = property(get_brands_profiles)
    last_activity = property(get_last_activity)
    start_time = property(get_start_time)

