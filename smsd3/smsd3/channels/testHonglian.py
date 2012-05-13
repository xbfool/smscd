# -*- coding: utf-8 -*-

import httplib, urllib
import copy
import timeit
setting = {
    'site':{
        'host': '219.238.160.81',
        'port': '80',
        'path': '/interface/limitnew.asp',
        'mode': 'POST',
    },
    'params':{
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
    }
}
def make_setting():
    s = copy.copy(setting)
    s['params']['phone']='18616820727'
    s['params']['message']='testhonglian'
    return s
def testSendHonglian():
    s = make_setting()
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params = urllib.urlencode(s['params'])
    conn = httplib.HTTPConnection(host=s['site']['host'],port=s['site']['port'])
    conn.request(s['site']['mode'], s['site']['path'], params, headers)
    response = conn.getresponse()
    print response.read().decode('gbk')

from timeit import Timer
#t = Timer("testSendHonglian()", "from __main__ import testSendHonglian")
#print t.timeit(1)
s = httplib.HTTPConnection('www.qidian.com')
s.request('','')
d = s.getresponse()
print d.status