#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import copy
import httplib, urllib
from urllib import urlencode
from urllib import quote
site_settings = {}

site_settings['honglian'] = {
    'host': '211.136.153.24',
    'path': '/qxtinterface/',
    'port': '80',
    'mode': 'POST',
    'sender': 'honglian',
}
site_settings['honglian_mock'] = {
    'host': '127.0.0.1',
    'path': '/interface/limitnew.asp',
    'port': '8000',
    'mode': 'POST',
    'sender': 'honglian'
}
  
site_settings['changshang_a'] = {
    'host': '123.196.114.68',
    'port': '8080',
    'path': '/sms_send2.do',
    'mode': 'POST',
    'sender': 'changshang_a'
}

site_settings['qixintong2012_106d'] = {
    'name': 'qixintong_106d',
    'host': '202.85.221.191',
    'path': '/mc/httpsendsms.php',
    'port': '80',
    'mode': 'GET',
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

config_settings['changshang_a_001'] = {
        'long_msg_support': True,
        'word_first_msg':'64',
        'word_per_msg':'64',
        'encoding':'gbk',
        'long_msg_split':False,
        'max_msg_words':70,
        'max_connection':1,
    }
config_settings['qixintong2012_106d_001'] = {
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
support_settings['cm'] = {
    'cm':True,
    'cu':False,
    'ct':False
}
support_settings['cu'] = {
    'cm':False,
    'cu':True,
    'ct':False
}
support_settings['ct'] = {
    'cm':False,
    'cu':False,
    'ct':True
}

settings = {}
settings['honglian_01'] = {
    'name': 'honglian_01',
    'desc': '移动106c',
    
    'site': site_settings['honglian'],
    'params':{
            'username':'jnfd',
            'password':'647185',
            'epid':'372',
    },
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],
    'queue':{
        'request':'channel.request.honglian_01',
        'response':'channel.response.honglian_01',
        'error':'channel.response.channel_error',
        'log':'channel.log.honglian_01',
    }
}

settings['honglian_bjyh'] = {
    'name': 'honglian_bjyh',
    'desc': '移动106c_bjyh',
    
    'site': site_settings['honglian'],

    'params':{
            'username':'jnfdbjyh',
            'password':'123456',
            'epid':'606',
    },
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],
    'queue':{
        'request':'channel.request.honglian_bjyh',
        'response':'channel.response.honglian_bjyh',
        'error':'channel.response.channel_error',
        'log':'channel.log.honglian_bjyh',
    }

}

settings['honglian_jtyh'] = {
    'name': 'honglian_jtyh',
    'desc': '移动106c_jtyh',
    
    'site': site_settings['honglian'],

    'params':{
            'username':'fdjtyh',
            'password':'123456',
            'epid':'607',
    },
    
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],
    
    'queue':{
        'request':'channel.request.honglian_jtyh',
        'response':'channel.response.honglian_jtyh',
        'error':'channel.response.channel_error',
        'log':'channel.log.honglian_jtyh',
    }

}

settings['honglian_ty'] = {
    'name': 'honglian_ty',
    'desc': '移动106c_ty',
    
    'site': site_settings['honglian'],
    'params':{
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
    },
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],
    'queue':{
        'request':'channel.request.honglian_ty',
        'response':'channel.response.honglian_ty',
        'error':'channel.response.channel_error',
        'log':'channel.log.honglian_ty',
    }

}

settings['honglian_tyb'] = {
    'name': 'honglian_tyb',
    'desc': '移动106c_tyb',
    
    'site': site_settings['honglian'],

    'params':{
            'username':'fdhz',
            'password':'123456',
            'epid':'6831',
    },
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],
    'queue':{
        'request':'channel.request.honglian_tyb',
        'response':'channel.response.honglian_tyb',
        'error':'channel.response.channel_error',
        'log':'channel.log.honglian_tyb',
    }

}

settings['honglian_tyd'] = {
    'name': 'honglian_tyd',
    'desc': '移动106c_tyd',
    
    'site': site_settings['honglian'],

    'params':{
            'user':'fdgg',
            'wd':'123456',
    },
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],
    'queue':{
        'request':'channel.request.honglian_tyd',
        'response':'channel.response.honglian_tyd',
        'error':'channel.response.channel_error',
        'log':'channel.log.honglian_tyd',
    }

}

settings['honglian_mock'] = {
    'name': 'honglian_mock',
    'desc': '移动106c_mock',
    
    'site': site_settings['honglian_mock'],
    'params':{
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
    },
    'config': config_settings['honglian_001'],
    'support': support_settings['all'],
    'queue':{
        'request':'channel.request.honglian_mock',
        'response':'channel.response.honglian_mock',
        'error':'channel.response.channel_error',
        'log':'channel.log.honglian_mock',
    }
}
import string
def send_honglian(addrs, msg, setting):
    s = setting
    s['params']['phone']= ';'.join(addrs)
    s['params']['message']= msg.decode('utf8').encode('gb2312')
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}

    params = urllib.urlencode(s['params'])
    #params = urllib.urlencode(s['params'])
    print params
    conn = httplib.HTTPConnection(host=s['site']['host'],port=s['site']['port'])
    path = s['site']['path'] + '?' + params
    #print s['site']['host'] + path

    conn.request('GET', path)
    
    #conn.request(s['site']['mode'], s['site']['path'], params, headers)
    response = conn.getresponse()
    return response.read().decode('gbk')

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
    ret = send_honglian(args.addrs, args.msg[0], settings['honglian_tyd'])
    process_ret(ret)
