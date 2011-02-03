import Queue
import string
import select

from itertools import cycle
from time import sleep

from lib.worker import Worker, ThreadWorker


class QueueManager(ThreadWorker):
    def __init__(self, *args, **kwargs):
        super(QueueManager, self).__init__(*args, **kwargs)
        self._queue = kwargs['queue']
        self._max_queue_gets_per_time = kwargs['max_queue_gets_per_time']

    def run(self):
        try:
            self._process()
        except:
            self._logger.exception('Thread failure')

    def _process(self):
        while self._is_running.value:
        #for asd in range(1):
            data = {
                '00000095': range(100),
                '00000004': string.ascii_lowercase,
                '00000069': ['abc', 'def', 'ghi', 'jkl']
            }.iteritems()

            for key, elements in data:
                self._logger.info('Processing queue %s' % (key))
                gets_count = 0
                for e in elements:
                    if gets_count > self._max_queue_gets_per_time:
                        self._logger.info('Switching queue')
                        break

                    try:
                        self._queue.put(key, e)

                    except Queue.Full:
                        self._logger.warning('%s Queue full' % (key))
                        break

                    else:
                        self._logger.info('Putting %s' % (e))
                        gets_count += 1


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
                self._logger.warning(self._queue.qsize())

                active_pipes, wp, we = select.select(self._pipes, [], [])

                for pipe in active_pipes:
                    if pipe.poll():
                        pipe.recv()

                        try:
                            data = self._queue.get()
                        except Queue.Empty:
                            self._logger.debug('Empty Queue')
                            break

                        else:
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
        self._max_size_per_queue = kwargs['max_size_per_queue']

    def put(self, key, value):
        if not self._queues.has_key(key):
            self._queues[key] = Queue.Queue(maxsize=self._max_size_per_queue)
            self._queues_keys.append(key)
            self._iter_queues_keys = cycle(self._queues_keys)

        self._queues[key].put(value, timeout=0)

    def get(self):
        for i in range(len(self._queues)):
            queue = self._queues[self._iter_queues_keys.next()]
            if queue.qsize():
                return queue.get(timeout=2)

        raise Queue.Empty

    def qsize(self):
        count = 0
        for k in self._queues.keys():
            count += self._queues[k].qsize()

        return count


class Director(Worker):
    def __init__(self, *args, **kwargs):
        super(Director, self).__init__(*args, **kwargs)
        self._queue = PartedQueue(max_size_per_queue=25)
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
                max_queue_gets_per_time=10,
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
