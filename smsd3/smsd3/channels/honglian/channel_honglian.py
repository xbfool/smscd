#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import simplejson as json
from honglian_queue import HonglianQueue


honglian_real_setting = {
    'site':{
        'host': '219.238.160.81',
        'path': '/interface/limitnew.asp',
        'port': '80',
        'mode': 'POST',
    },
    'params':{
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
    }
}

honglian_mock_setting = {
    'site':{
        'host': '127.0.0.1',
        'path': '/interface/limitnew.asp',
        'port': '8000',
        'mode': 'POST',
    },
    'params':{
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
    }
}


def make_param(body):
    s = copy.copy(honglian_mock_setting)
    s['params']['phone']= body['addr']
    s['params']['message']= body['msg']
    return s
    
def send_honglian(body):
    print body
    s = make_param(body)
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params = urllib.urlencode(s['params'])
    conn = httplib.HTTPConnection(host=s['site']['host'],port=s['site']['port'])
    conn.request(s['site']['mode'], s['site']['path'], params, headers)
    response = conn.getresponse()
    return response.read().decode('gbk')

def parse_response(ch, method, properties, body):
    o =  json.loads(body)
    ret = send_honglian(o)
    print ret

def run():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='debian'))
    channel = connection.channel()
    channel.queue_declare(queue=HonglianQueue.recv_queue)
    channel.basic_consume(parse_response,
                          queue=HonglianQueue.recv_queue,
                          no_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    run()