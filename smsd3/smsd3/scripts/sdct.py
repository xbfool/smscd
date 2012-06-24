#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import copy
import httplib, urllib
from urllib import urlencode
from urllib import quote

def send_sdct():
    params_d ={}
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params_d['uid'] = '15305374505'
    params_d['pwd'] = '12345678'
    params_d['address'] = '18906413323'
    params_d['content'] = 'test sd ct'
    params = urllib.urlencode(params_d)
    host = '219.146.6.117'
    path = '/AIS/HTTPService/SendSMS.aspx'
    conn = httplib.HTTPConnection(host=host)

    
    conn.request('POST', path, params, headers)
    response = conn.getresponse()
    return response.read()

def parse_arg():
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--msg', metavar='Message', type=str, nargs=1,
                       help='phonenumber')
    parser.add_argument('--addrs', nargs='*')

    args = parser.parse_args()
    return args

import urllib
def process_ret(ret):
    s = urllib.unquote(ret).decode('utf8')
    print s
if __name__ == '__main__':
    #args = parse_arg()
    ret = send_sdct()
    process_ret(ret)
