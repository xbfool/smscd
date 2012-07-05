#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import copy
import httplib, urllib


site_settings = {}

site_settings['zhangshangtong'] = {
    'host': 'pi.f3.cn',
    'path': '/SendSMS.aspx',
    'port': '80',
    'mode': 'POST',
    'sender': 'zhangshangtong',
}
config_settings = {}

config_settings['zhangshangtong_01'] = {
        'long_msg_support': True,
        'word_first_msg':'64',
        'word_per_msg':'64',
        'encoding':'utf8',
        'long_msg_split':False,
        'max_msg_words':70,
        'max_connection':1,
    }
support_settings = {}
support_settings['all'] = {
    'cm':True,
    'cu':True,
    'ct':True
}

settings = {}

settings['zhangshangtong_01'] = {
    'name': 'zhangshangtong_01',
    'desc': '移动106d_01',
    
    'site': site_settings['zhangshangtong'],
    'config': config_settings['zhangshangtong_01'],
    'support': support_settings['all'],

    'params':{
            'ececcid':'305555004',
            'password':'abc123',
            'msgtype':'5',
            'longcode':'',
    },
}



def send_zhangshangtong(addrs, msg, setting):
    s = setting
    s['params']['msisdn']= ','.join(addrs)
    s['params']['smscontent']= msg.decode('utf8').encode(s['config']['encoding'])

    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params = urllib.urlencode(s['params'])
    print params
    conn = httplib.HTTPConnection(host=s['site']['host'],port=s['site']['port'])
    conn.request(s['site']['mode'], s['site']['path'], params, headers)
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

def process_ret(ret):
    print ret
if __name__ == '__main__':
    args = parse_arg()
    ret = send_zhangshangtong(args.addrs, args.msg[0], settings['zhangshangtong_01'])
    process_ret(ret);
