# -*- coding: utf-8 -*-
import signal

from multiprocessing import Queue, Manager

from lib.daemon import Daemon
from lib.file_queue import FileQueue


class SnoopyDaemon(Daemon):
    """
    """

    def __init__(self, pid, cfg, log):
        Daemon.__init__(self, pid)
        self._cfg = cfg
        self._log = log
        self._worker = worker

    def stop(self, *args, **kargs):
        self._proc_running.set(False)
        self._is_running = False

    def run(self):
        try:
            signal.signal(signal.SIGTERM, self.stop)

            self._proc_running = Manager().Value(bool, True)
            self._queue = Queue()

            self._processes = []
            self._processes.append(
                FileQueue(self._cfg['pool'], self._queue,
                    self._proc_running, self.log))

            for x in range(self._cfg['processes']):
                self._processes.append(
                FileQueue(self._cfg['pool'], self._queue,
                    self._proc_running, self.log))
                ########)

            [x.start() for x in self._processes]
            self._is_running = True

            self._log.info('I\'m ready, Sir!')

            while self._is_running:
                try:
                    signal.pause()
                except:
                    continue

            [x.join() for x in self._processes]

            self._log.info('Goodby, Sir!')

        except Exception, e:
            self._log.excepttion('General failure.')
            raise e
