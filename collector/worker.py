import Queue
import string
import select
import msgpack
from threading import Event

from itertools import cycle
from time import sleep
from random import random
from amqplib.client_0_8 import Message, AMQPConnectionException

from lib.worker import Worker, ThreadWorker
from lib.rabbit_handler import RabbitHandler, RabbitEmpty
from collector.process import CollectorProcess


class QueueManager(ThreadWorker):
    def __init__(self, *args, **kwargs):
        super(QueueManager, self).__init__(*args, **kwargs)
        self._queue = kwargs['queue']
        self._max_queue_gets_per_time = kwargs['max_queue_gets_per_time']
        self._queueman_is_running = kwargs['queueman_is_running']
        self._rabbit_cfg = kwargs['rabbit_cfg']
        self._know_queues = kwargs['know_queues']

        self._rabbit = RabbitHandler(**self._rabbit_cfg)

    def run(self):
        try:
            self._process()
        except:
            self._logger.exception('Thread failure')

    def _process(self):

        while self._is_running.value:
            queues_puts_sum = 0

            for queue in self._know_queues:
                self._logger.info('Processing queue %s' % (queue))

                queue_puts = 0
                for i in range(self._max_queue_gets_per_time):
                    try:
                        data = self._rabbit.get(queue)
                        self._queue.put(queue, data)

                    except Queue.Full:
                        self._rabbit.reject()
                        self._logger.warning('%s Queue full' % (queue))
                        break

                    except RabbitEmpty:
                        self._logger.warning('%s Queue empty' % (queue))
                        break

                    except AMQPConnectionException:
                        self._rabbit.disconnect()

                    except Exception, e:
                        self._logger.exception('Error %s' % (e))
                        self._logger.warning('----------------------------')

                    else:
                        self._rabbit.ack()
                        queue_puts += 1

                queues_puts_sum += queue_puts
                self._logger.info('%d elements puts' % (queue_puts))
                self._logger.info('Switching queue')

            if queues_puts_sum == 0:
                sleep(5)

        self._rabbit.disconnect()
        self._queueman_is_running.clear()
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
                active_pipes, wp, we = select.select(self._pipes, [], [], 2)

                for pipe in active_pipes:
                    if pipe.poll():
                        pipe.recv()

                        try:
                            data = self._queue.get()
                        except Queue.Empty:
                            self._logger.debug('Empty Queue')
                            pipe.send('empty')
                        else:
                            pipe.send(data)

            else:
                if (
                    not self._is_running.value and
                    not self._queueman_is_running.is_set()
                ):
                    for pipe in self._pipes:
                        self._logger.debug('Closing worker')
                        pipe.send('close')

                    break

                else:
                    sleep(5)


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
        self._cfg = kwargs['cfg']
        self._queue = PartedQueue(
            max_size_per_queue=self._cfg['max_size_per_queue']
        )
        self._pipes = kwargs['pipes']

    def run(self):
        self._logger.info('Ready to work')
        try:
            self._process()
        except:
            self._logger.exception('eee')

    def _process(self):
        self._queueman_is_running = Event()
        self._queueman_is_running.set()

        self._threads = []
        self._threads.append(
            QueueManager(
                name='snoopy-director-queman',
                queue=self._queue,
                max_queue_gets_per_time=self._cfg['max_queue_gets_per_time'],
                rabbit_cfg=self._cfg['rabbit_cfg'],
                know_queues=self._cfg['know_queues'],
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
                sleep(1)
                #signal.pause()
            except:
                continue

        [t.join() for t in self._threads]

        self._logger.info('Goodbye!')


class Collector(Worker):
    def __init__(self, *args, **kwargs):
        super(Collector, self).__init__(*args, **kwargs)
        self._pipe = kwargs['pipe']
        self._rabbit_cfg = kwargs['rabbit_cfg']
        self._rabbit_sc_cfg = kwargs['rabbit_sc_cfg']

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
                        rabbit_cfg=self._rabbit_cfg,
                        rabbit_sc_cfg=self._rabbit_sc_cfg,
                        dispatch_info=data['dispatch_info'],
                        cco_profile=data['cco_profile'],
                        dispatch_content=data.get('dispatch_content')
                    )

                except KeyError, TypeError:
                    self._logger.error('Invalid format')

                else:
                    charge_id = data['cco_profile']['charge_id']
                    try:
                        pepe.cco_charge()

                        if pepe.is_cco_charge_ok():
                            self._logger.info('[%s] Charge OK' % (charge_id))
                            pepe.club_notify()

                        else:
                            self._logger.info('[%s] Charge FAIL' % (charge_id))
                            if pepe.is_async_fallbackeable():
                                pepe.sct_async_charge()

                        self._logger.info('[%s] Reporting to Snoopy ' \
                            'Charges.' % (charge_id))
                        pepe.report_charge()

                        if pepe.ignore_charge_result():
                            self._logger.info('[%s] Dispatch sended ' \
                                'ignoring charge result.' % (charge_id))
                        else:
                            if pepe.is_dispatch_sendeable():
                                pepe.enable_dispatch_delivery()
                            else:
                                self._logger.info('[%s] Dispatch discarded ' \
                                    'to %s' % (charge_id, pepe.msisdn))

                    except:
                        self._logger.exception('[%s] Reinjecting to queue' % (
                            charge_id))
                        rabbit = RabbitHandler(**self._rabbit_cfg)
                        rabbit.reinject(message)
                        rabbit.disconnect()

                finally:
                    self._logger.info('Done.')

            elif message == 'empty':
                sleep(5)

            elif message == 'close':
                break

        self._logger.info('Goodbye!')
