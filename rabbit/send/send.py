#!/usr/bin/env python

import pika
import datetime


creds = pika.credentials.PlainCredentials('admin', 'admin', erase_on_connect=False)
connection = pika.BlockingConnection(pika.ConnectionParameters(

        host='104.42.181.68', credentials=creds))

channel = connection.channel()
channel.queue_declare(queue='hello')

start = datetime.datetime.now()
for i in range(5000):
        channel.basic_publish(exchange='',

                        routing_key='hello',

                        body='Hello PyWorld! '+i)

        print(" [x] Sent 'Hello PyWorld!' "+i)
end = datetime.datetime.now()
print("total time in ms"+(end-start))
connection.close()