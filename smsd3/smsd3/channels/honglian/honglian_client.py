#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import simplejson as json
from itertools import count
from honglian_queue import HonglianQueue
msg = {
    'addr':'18616820727',
    'msg':'haha'
}
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'debian'))
channel = connection.channel()

channel.queue_declare(queue=HonglianQueue.recv_queue)

channel.basic_publish(exchange='',
                      routing_key=HonglianQueue.recv_queue,
                      body=json.dumps(msg))
                          

