from multiprocessing import Process
from threading import Thread

from lib.logger import get_logger


class Worker(Process):
    def __init__(self, *args, **kwargs):
        Process.__init__(self)

        log_name = kwargs.get('name', 'snoopy_no_name')
        if isinstance(kwargs.get('proc_num'), int):
            log_name = '%s[%0.2d]' % (log_name, kwargs.get('proc_num'))

        self._logger = get_logger(log_name)
        self._logger.info('Initializing...')

        self._is_running = kwargs['is_running']

    def run(self):
        raise NotImplemented('This method should be programmed.')


class ThreadWorker(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self)

        self._logger = get_logger(kwargs.get('name', 'snoopy_thread'))
        self._logger.info('Initializing...')

        self._is_running = kwargs['is_running']

    def run(self):
        raise NotImplemented('This method should be programmed.')
