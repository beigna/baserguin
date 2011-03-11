from multiprocessing import Value, Pipe
import os
import signal
import sys

from collector.worker import Director, Collector
from lib.daemon import Daemon
from lib.logger import get_logger
from lib.load_conf import load_conf


class CollectorDaemon(Daemon):
    def __init__(self, cfg):
        self._cfg = cfg
        Daemon.__init__(self, self._cfg['pid_path'])
        self._logger = get_logger('snoopy-collector')

    def stop(self, *args, **kargs):
        self._is_running.value = False

    def run(self):
        try:
            signal.signal(signal.SIGTERM, self.stop)

            self._is_running = Value('b', True)

            self._processes = []
            self._collector_pipes = []

            for proc_num in range(self._cfg['workers_num']):
                p, c = Pipe()

                self._collector_pipes.append(p)

                self._processes.append(
                    Collector(
                        name='snoopy-collector-col',
                        pipe=c,
                        proc_num=proc_num,
                        rabbit_cfg=self._cfg['rabbit_cfg'],
                        is_running=self._is_running
                    )
                )

            self._processes.append(
                Director(
                    name='snoopy-collector-dir',
                    pipes=self._collector_pipes,
                    cfg=self._cfg,
                    is_running=self._is_running
                )
            )

            [p.start() for p in self._processes]

            self._logger.info('I\'m ready!')

            while self._is_running.value:
                try:
                    signal.pause()
                except:
                    continue

            [p.join() for p in self._processes]

            self._logger.info('Finalised shutdown.')

        except:
            self._logger.exception('General failure')

if __name__ == '__main__':
    conf = load_conf('%s/conf/collector.json' % (os.path.abspath(sys.path[0])))

    d = CollectorDaemon(conf)
    d.start()
