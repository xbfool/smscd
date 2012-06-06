#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import copy
import httplib, urllib


site_settings = {}

site_settings['honglian'] = {
    'host': '202.85.221.191',
    'path': '/mc/httpsendsms.php',
    'port': '80',
    'mode': 'POST',
    'sender': 'qixintong2012',
}
config_settings = {}

config_settings['honglian_001'] = {
        'long_msg_support': True,
        'word_first_msg':'64',
        'word_per_msg':'64',
        'encoding':'gbk',
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

settings['qixintong2012_01'] = {
    'name': 'qixintong2012_01',
    'desc': '移动106d_01',
    
    'site': site_settings['honglian'],
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],

    'params':{
            'ua':'cjcsd',
            'pw':'1234',
    },
}

settings['qixintong2012_02'] = {
    'name': 'qixintong2012_01',
    'desc': '移动106d_01',
    
    'site': site_settings['honglian'],
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],

    'params':{
            'ua':'sdcjc',
            'pw':'318340',
    },
}

def send_qixintong2012(addrs, msg, setting):
    s = setting
    s['params']['mobile']= ','.join(addrs)
    s['params']['msg']= msg.decode('utf8').encode(s['config']['encoding'])
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params = urllib.urlencode(s['params'])
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
    if ret == '00':
        print '发送成功'
    else:
        print ret
if __name__ == '__main__':
    args = parse_arg()
    if  args.addrs != None and len(args.addrs) > 0 and len(args.msg[0]):
        ret = send_qixintong2012(args.addrs, args.msg[0], settings['qixintong2012_02'])
        process_ret(ret)
    else:
        print args
        pass
