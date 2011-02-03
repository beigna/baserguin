import Queue
import string

from itertools import cycle
from time import sleep

from lib.worker import Worker, ThreadWorker


class QueueManager(ThreadWorker):
    def __init__(self, *args, **kwargs):
        super(QueueManager, self).__init__(*args, **kwargs)
        self._queue = kwargs['queue']

    def run(self):
        try:
            self._process()
        except:
            self._logger.exception('Thread failure')

    def _process(self):
        while self._is_running.value:
            data = {
                '00000095': range(100),
                #'00000004': string.ascii_lowercase,
                #'00000069': ['abc', 'def', 'ghi', 'jkl']
            }.iteritems()

            for key, elements in data:
                self._logger.info('Processing queue %s' % (key))
                for e in elements:
                    try:
                        self._queue.put(key, e)

                    except Queue.Full:
                        self._logger.warning('%s Queue full' % (key))
                        break

                    else:
                        self._logger.info('Putting %s' % (e))

        self._logger.info('Goodbye!')


class PipeManager(ThreadWorker):
    def __init__(self, *args, **kwargs):
        super(PipeManager, self).__init__(*args, **kwargs)
        self._queue = kwargs['queue']
        self._pipes = kwargs['pipes']

    def run(self):
        self._logger.info('Ready to work')
        try:
            self._process()
        except:
            self._logger.exception('Thread failure')

    def _process(self):
        while True:
            if self._queue.qsize():
                for pipe in self._pipes:
                    if pipe.poll():
                        pipe.recv()
                        self._logger.debug('---------MEPIDIERON')

                        try:
                            data = self._queue.get()
                        except Queue.Empty:
                            self._logger.debug('Empty Queue')

                        else:
                            self._logger.debug('---------MANDO')
                            pipe.send(data)

            if not self._is_running.value and not self._queue.qsize():
                for pipe in self._pipes:
                    self._logger.debug('Closing worker')
                    pipe.send('close')

                break


class PartedQueue(object):
    def __init__(self, *args, **kwargs):
        self._queues = {}
        self._queues_keys = []
        self._iter_queues_keys = cycle([])

    def put(self, key, value):
        if not self._queues.has_key(key):
            self._queues[key] = Queue.Queue(maxsize=10)
            self._queues_keys.append(key)
            self._iter_queues_keys = cycle(self._queues_keys)

        self._queues[key].put(value, timeout=0)

    def get(self):
        data = self._queues[self._iter_queues_keys.next()].get(timeout=2)
        return data

    def qsize(self):
        count = 0
        for k in self._queues.keys():
            count += self._queues[k].qsize()

        return count


class Director(Worker):
    def __init__(self, *args, **kwargs):
        super(Director, self).__init__(*args, **kwargs)
        self._queue = PartedQueue()
        self._pipes = kwargs['pipes']

    def run(self):
        self._logger.info('Ready to work')
        try:
            self._process()
        except:
            self._logger.exception('eee')

    def _process(self):
        self._threads = []
        self._threads.append(
            QueueManager(
                name='snoopy-director-queman',
                queue=self._queue,
                is_running=self._is_running
            )
        )
        self._threads.append(
            PipeManager(
                name='snoopy-director-pipman',
                queue=self._queue,
                pipes=self._pipes,
                is_running=self._is_running
            )
        )

        [t.start() for t in self._threads]

        while self._is_running.value:
            try:
                signal.pause()
            except:
                continue

        [t.join() for t in self._threads]

        self._logger.info('Goodbye!')

    def _refill_queue(self, queue):
        self._logger.info('Queue: %s' % (queue))


class Collector(Worker):
    def __init__(self, *args, **kwargs):
        super(Collector, self).__init__(*args, **kwargs)
        self._pipe = kwargs['pipe']

    def run(self):
        self._logger.info('Ready to work')

        try:
            self._process()
        except:
            self._logger.exception('eee')

    def _process(self):
        while True:
            self._pipe.send('gimme')

            message = self._pipe.recv()

            if message == 'close':
                break
            else:
                self._logger.info('Charging %s' % (message))

        self._logger.info('Goodbye!')
