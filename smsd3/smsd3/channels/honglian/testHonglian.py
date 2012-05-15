# -*- coding: utf-8 -*-

import httplib, urllib
import copy
import timeit
honglian_setting = {
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

def make_param(body):
    s = copy.copy(honglian_setting)
    s['params']['phone']= body['addr']
    s['params']['message']= body['msg']
    return s
    
def send_honglian(body):
    s = make_param(body)
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params = urllib.urlencode(s['params'])
    conn = httplib.HTTPConnection(host=s['site']['host'],port=s['site']['port'])
    conn.request(s['site']['mode'], s['site']['path'], params, headers)
    response = conn.getresponse()
    return response.read().decode('gbk')
    
if __name__ == '__main__':
    from timeit import Timer
    print send_honglian({"addr":'18616820727','msg':'123456'})
    #t = Timer("testSendHonglian()", "from __main__ import testSendHonglian")
    #print t.timeit(1)
