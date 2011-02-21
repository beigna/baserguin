import Queue
import string
import select
import msgpack

from itertools import cycle
from time import sleep
from amqplib.client_0_8 import Message

from lib.worker import Worker, ThreadWorker
from lib.rabbit_handler import RabbitHandler, RabbitEmpty
from collector.process import CollectorProcess


RABBIT_CFG = {
    'host': '192.168.23.236',
    'userid': 'snoopy',
    'password': 'snoopy',
    'virtual_host': '/snoopy'
}


class QueueManager(ThreadWorker):
    def __init__(self, *args, **kwargs):
        super(QueueManager, self).__init__(*args, **kwargs)
        self._queue = kwargs['queue']
        self._max_queue_gets_per_time = kwargs['max_queue_gets_per_time']
        self._queueman_is_running = kwargs['queueman_is_running']

        self._rabbit = RabbitHandler(**RABBIT_CFG)

    def run(self):
        try:
            self._process()
        except:
            self._logger.exception('Thread failure')

    def _process(self):
        know_queues = [
            'charges_00000069',
            'charges_00000045',
            'charges_00000036',
            'charges_00000051',
            'charges_00000057',
            'charges_00000004',
            'charges_00000003',
            'charges_00000095',
            'charges_00000059',
        ]

        while self._is_running.value:
        # ACa se pudre la mondiola
            for queue in know_queues:
                self._logger.info('Processing queue %s' % (queue))

                for i in range(self._max_queue_gets_per_time):
                    try:
                        data = self._rabbit.get(queue)
                        self._queue.put(queue, data)

                    except Queue.Full:
                        self._logger.warning('%s Queue full' % (queue))
                        break

                    except RabbitEmpty:
                        self._logger.warning('%s Queue empty' % (queue))
                        break

                    except Exception, e:
                        self._logger.exception('Error %s' % (e))

                    else:
                        self._logger.info('Putting %s' % (type(data)))
                        self._rabbit.ack()


                self._logger.info('Switching queue')

            sleep(1)

        self._rabbit.disconnect()
        self._queueman_is_running = False
        self._logger.info('Goodbye!')


class PipeManager(ThreadWorker):
    def __init__(self, *args, **kwargs):
        super(PipeManager, self).__init__(*args, **kwargs)
        self._queue = kwargs['queue']
        self._pipes = kwargs['pipes']
        self._queueman_is_running = kwargs['queueman_is_running']

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

            if not self._is_running.value \
            and not self._queue.qsize() \
            and not self._queueman_is_running:
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
        self._queue = PartedQueue(max_size_per_queue=5)
        self._pipes = kwargs['pipes']

    def run(self):
        self._logger.info('Ready to work')
        try:
            self._process()
        except:
            self._logger.exception('eee')

    def _process(self):
        self._queueman_is_running = True

        self._threads = []
        self._threads.append(
            QueueManager(
                name='snoopy-director-queman',
                queue=self._queue,
                max_queue_gets_per_time=5,
                queueman_is_running = self._queueman_is_running,
                is_running=self._is_running
            )
        )
        self._threads.append(
            PipeManager(
                name='snoopy-director-pipman',
                queue=self._queue,
                pipes=self._pipes,
                queueman_is_running = self._queueman_is_running,
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

            if isinstance(message, Message):
                try:
                    self._logger.info('Processing charge...')
                    data = msgpack.loads(message.body)

                    pepe = CollectorProcess(
                        logger=self._logger,
                        dispatch_info=data['dispatch_info'],
                        cco_profile=data['cco_profile'],
                        dispatch_content=data.get('dispatch_content')
                    )

                    pepe.cco_charge()

                    if pepe.is_cco_charge_ok():
                        self._logger.info('Charge OK')
                        pepe.club_notify()

                    else:
                        self._logger.info('Charge FAIL')
                        if pepe.is_async_fallbackeable():
                            pepe.sct_async_charge()

                    if pepe.ignore_charge_result():
                        self._logger.info('Dispatch sended ignoring charge '\
                            'result.')
                    else:
                        if pepe.is_dispatch_sendeable():
                            pepe.enable_dispatch_send()
                        else:
                            self._logger.info('Dispatch discarded to %s' % (
                                pepe.msisdn
                            ))

                except:
                    #Reencolo
                    rabbit = RabbitHandler(**RABBIT_CFG)
                    rabbit.reinject(message)
                    rabbit.disconnect()

            else:
                if message == 'close':
                    break

            sleep(1)
        self._logger.info('Goodbye!')
