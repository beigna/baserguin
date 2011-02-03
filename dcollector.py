from multiprocessing import Value, Pipe
import signal
import os

from collector.worker import Director, Collector
from lib.daemon import Daemon
from lib.logger import get_logger


class CollectorDaemon(Daemon):
    def __init__(self, pid_path):
        Daemon.__init__(self, pid_path)
        self._logger = get_logger('snoopy-collector')

    def stop(self, *args, **kargs):
        self._is_running.value = False

    def run(self):
        try:
            signal.signal(signal.SIGTERM, self.stop)

            self._is_running = Value('b', True)

            self._processes = []
            self._collector_pipes = []

            for proc_num in range(5):
                p, c = Pipe()

                self._collector_pipes.append(p)

                self._processes.append(
                    Collector(
                        name='snoopy-collector-col',
                        pipe=c,
                        proc_num=proc_num,
                        is_running=self._is_running
                    )
                )

            self._processes.append(
                Director(
                    name='snoopy-collector-dir',
                    pipes=self._collector_pipes,
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
    d = CollectorDaemon('/tmp/collector.pid')
    d.start()
