import sys
import msgpack

from amqplib import client_0_8 as amqp


conn = amqp.Connection(host='192.168.23.236')
chan = conn.channel()

c = 0

while True:
    msg = chan.basic_get(sys.argv[1])

    try:
        print msg.delivery_info
        #print msg.body

        try:
            #data = msgpack.loads(msg.body)
            #print data
            pass
        except: pass

        chan.basic_ack(msg.delivery_tag)
        c += 1

    except AttributeError:
        print 'vacio'
        break

print c

