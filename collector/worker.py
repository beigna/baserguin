import Queue
import string

from itertools import cycle
from time import sleep

from lib.worker import Worker


class PartedQueue(object):
    def __init__(self, *args, **kwargs):
        self._queues = {}
        self._queues_keys = []
        self._iter_queues_keys = cycle([])

    def put(self, key, value):
        if not self._queues.has_key(key):
            self._queues[key] = Queue.Queue(maxsize=2)
            self._queues_keys.append(key)
            self._iter_queues_keys = cycle(self._queues_keys)

        self._queues[key].put(value, timeout=0)

    def get(self):
        return self._queues[self._iter_queues_keys.next()].get()

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
        if self._is_running.value:
            for key, elements in self._get_queues():
                self._logger.info('Processing queue %s' % (key))
                for e in elements:
                    try:
                        self._queue.put(key, e)
                    except Queue.Full:
                        self._logger.warning('%s Queue full' % (key))
                        break

                    else:
                        self._logger.info('Putting %s' % (e))


            while self._queue.qsize():
                for pipe in self._pipes:
                    if pipe.poll():
                        pipe.recv()
                        pipe.send(self._queue.get())

    def _get_queues(self):
        return {
            '00000095': range(10),
            '00000004': string.ascii_lowercase,
        }.iteritems()

    def _refill_queue(self, queue):
        self._logger.info('Queue: %s' % (queue))


class Collector(Worker):
    def __init__(self, *args, **kwargs):
        super(Collector, self).__init__(*args, **kwargs)
        self._pipe = kwargs['pipe']

    def run(self):
        self._logger.info('Ready to work')

        while not self._pipe.closed:
            self._pipe.send('gimme')

            if self._pipe.poll():
                self._logger.info('Charging %s' % (self._pipe.recv()))

            sleep(1)
