from amqplib import client_0_8 as amqp
import glob
from ConfigParser import ConfigParser

#conn = amqp.Connection(host='192.168.149.140', userid='snoopy', password='Sn00py_P012', virtual_host='/snoopy')
conn = amqp.Connection(host='192.168.149.140')
chan = conn.channel()

brands_dir = '/etc/opt/cyclelogic/snoopy_xms/brands_profiles/*.conf'
config = ConfigParser()
charge_queue_name_list = []

for current_file in glob.glob(brands_dir):
    config.read(current_file)
    charge_queue_name_list.append('charges_%s' % config.get('General', 'BrandId'))

chan.exchange_declare(exchange='x', type='direct', durable=True, auto_delete=False)

for charge_queue_name in charge_queue_name_list:
    print charge_queue_name
    chan.queue_declare(queue=charge_queue_name, durable=True, exclusive=False, auto_delete=False)
    chan.queue_bind(queue=charge_queue_name, exchange='x',
            routing_key=charge_queue_name)

chan.queue_declare(queue='stats', durable=True, exclusive=False, auto_delete=False)
chan.queue_bind(queue='stats', exchange='x', routing_key='stats')

chan.queue_declare(queue='putter', durable=True, exclusive=False, auto_delete=False)
chan.queue_bind(queue='putter', exchange='x', routing_key='putter')

chan.close()
conn.close()
