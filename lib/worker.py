from multiprocessing import Process

from lib.logger import get_logger


class Worker(Process):
    def __init__(self, *args, **kwargs):
        Process.__init__(self)

        self._logger = get_logger(kwargs.get('name', 'snoopy_no_name'))
        self._logger.info('Initializing...')

        self._is_running = kwargs['is_running']

    def run(self):
        raise NotImplemented('This method should be programmed.')

