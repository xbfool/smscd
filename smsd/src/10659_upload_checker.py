#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import httplib, urllib
import time
from xml.etree.ElementTree import fromstring, ElementTree
import httplib
url = '127.0.0.1:8888'

def send_sdct():
    params_d ={}
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params_d['username'] = '15305374505'
    params_d['password'] = '12345678'
    params = urllib.urlencode(params_d)
    host = '219.146.6.117'
    path = '/AIS/HTTPService/Receive.aspx'
    conn = httplib.HTTPConnection(host=host)

    
    conn.request('POST', path, params, headers)
    response = conn.getresponse()
    return response.read()


def process_ret(ret):
    s = urllib.unquote(ret)
    b = s.replace('+', ' ')
    b = '''<Reply errorCode='0'><Message mobile="测试" content="b" receivetime="c"></Message></Reply>'''
    tree = ElementTree(fromstring(b))
    doc = tree.getroot()
    c = doc.findall('Message')
    if not c:
        return
    
    try:
        conn = httplib.HTTPConnection(url)
    except:
        return

    
    for i in c:
        mobile = i.get('mobile')
        content = i.get('content')
        receivetime = i.get('receivetime')
        params = {
                  'mobile':mobile.encode('utf8'),
                  'content':content.encode('utf8'),
                  'receivetime':receivetime.encode('utf8')
                  }
        print params
        path = urllib.urlencode(params)
        conn.request('GET', path)
        response = conn.getresponse()
        response.read()
if __name__ == '__main__':
    while 1:
        try:
            ret = send_sdct()
            process_ret(ret)
        except:
            pass
        time.sleep(10)
