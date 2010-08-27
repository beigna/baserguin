# -*- coding: utf-8 -*-

import sys
import os
from multiprocessing import Process
import Queue # for Queue.Empty exception
from ConfigParser import ConfigParser
import simplejson

from lib.snoopy_types import SnoopyDispatch

class Newser(Process):
    def __init__(self, queue, is_running, process_id, cfg, log):
        Process.__init__(self)
        self._queue = queue
        self._is_running = running
        self._procces_id = process_id
        self._cfg = cfg
        self._log = log
        self._dc = {1: 'SMS', 3: 'MMS', 5: 'WAP'}

    @staticmethod
    def load_settings(log):
        try:
            file_path = '%s/conf/newser.conf' % (os.path.abspath(sys.path[0]))

            if not os.path.exists(file_path):
                raise IOError('%s do not exists.' % file_path)

            config = ConfigParser()
            config.read(file_path)

            cfg = {}

            cfg['pid_path'] = config.get('General', 'Pid')
            cfg['processes'] = config.getint('General', 'Processes')
            cfg['pool_inlet'] = config.get('General', 'PoolInlet')
            cfg['pool_outlet'] = config.get('General', 'PoolOutlet')
            cfg['reports_outlet'] = config.get('General', 'ReportsOutlet')

            return cfg

        except Exception, e:
            log.exception('Error load settings.')
            raise e

    def run(self):
        while self._is_running.get() or not self._queue.empty():
            try:
                file_path = self._queue.get(timeout=2)
            except Queue.Empty:
                continue

            try:
                self._process(file_path)
            except Exception, e:
                try:
                    self.log.exception('#%02d Re enqueueing the failed ' \
                        'file.' % (self._procces_id))
                    os.rename(file_path, file_path.replace('.proc', '.go'))
                except:
                    self.log.exception('#%02d File was not re ' \
                        'enqueued' % (self._procces_id))

    def _process(self, file_path):
        try:
            fp = open(file_path, 'r')
            data = simplejson.load(fp)
            fp.close()

            dispatch = SnoopyDispatch()
            dispatch.from_dict(data)

        except Exception, e:
            self._log.exception('#%02d %s Dispatch could not be loaded.' % (
                self._procces_id))
            raise e

        editormm = EditorMM(self._log)
        channel = editormm.get_channel(dispatch.channel_id)

        news = editormm.get_news(dispatch)


