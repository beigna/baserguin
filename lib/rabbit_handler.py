from amqplib import client_0_8 as amqp


class RabbitEmpty(Exception):
    pass


class RabbitHandler(object):
    def __init__(self, *args, **kwargs):
        self._host = kwargs['host']
        self._userid = kwargs['userid']
        self._password = kwargs['password']
        self._virtual_host = kwargs['virtual_host']

        self._use_transaction = kwargs.get('use_transaction', False)
        self._conn = None

    def connect(self):
        self._conn = amqp.Connection(
            host=self._host,
            userid=self._userid,
            password=self._password,
            virtual_host=self._virtual_host
        )

        self._chan = self._conn.channel()

        if self._use_transaction:
            self._chan.tx_select()

    def disconnect(self):
        try: self._chan.close()
        except: pass
        try: self._conn.close()
        except: pass
        self._conn = None

    def put(self, data, exchange='', routing_key=''):
        if not self._conn:
            self.connect()

        msg = amqp.Message(data, delivery_mode=2)
        self._chan.basic_publish(
            msg, exchange=exchange,
            routing_key=routing_key
        )

    def get(self, queue_name):
        if not self._conn:
            self.connect()

        msg = self._chan.basic_get(queue_name)
        if msg:
            self._msg = msg
            return self._msg

        raise RabbitEmpty('Empty queue.')

    def ack(self):
        self._chan.basic_ack(self._msg.delivery_tag)

    def reinject(self, message):
        self.put(
            data=message.body,
            exchange=message.delivery_info['exchange'],
            routing_key=message.delivery_info['routing_key']
        )

    def commit(self):
        self._chan.tx_commit()

    def rollback(self):
        self._chan._tx_rollback()

    def discard(self):
        self._chan.basic_reject(
            delivery_tag=self._msg.delivery_tag,
            requeue=False
        )

    def reject(self):
        self._chan.basic_reject(
            delivery_tag=self._msg.delivery_tag,
            requeue=True
        )
