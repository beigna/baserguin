from amqplib import client_0_8 as amqp

conn = amqp.Connection(host='192.168.23.236', userid='snoopy', password='snoopy', virtual_host='/snoopy')
chan = conn.channel()

chan.queue_declare(queue='charges', durable=True, exclusive=False, auto_delete=False)
chan.queue_declare(queue='putter', durable=True, exclusive=False, auto_delete=False)

chan.exchange_declare(exchange='x', type='direct', durable=True, auto_delete=False)

chan.queue_bind(queue='charges', exchange='x', routing_key='charges')
chan.queue_bind(queue='putter', exchange='x', routing_key='putter')

#msg = amqp.Message('hola1', delivery_mode=2)
#chan.basic_publish(msg, exchange='gilada', routing_key='pepe')
#chan.basic_publish(msg, exchange='', routing_key='')

chan.close()
conn.close()

