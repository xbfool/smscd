#!/usr/bin/env python
# -*- coding: utf-8 -*-
site_settings = {}

site_settings['honglian'] = {
    'host': '219.238.160.81',
    'path': '/interface/limitnew.asp',
    'port': '80',
    'mode': 'POST',
}
site_settings['honglian_mock'] = {
    'host': '127.0.0.1',
    'path': '/interface/limitnew.asp',
    'port': '8000',
    'mode': 'POST',
}
  
  
site_settings['changshang_a'] = {
    'host': '123.196.114.68',
    'port': '8080',
    'path': '/sms_send2.do',
    'mode': 'POST',
        
}

config_settings = {}

config_settings['honglian_001'] = {
        'long_msg_support': True,
        'word_first_msg':'64',
        'word_per_msg':'64',
        'encoding':'gbk',
        'long_msg_split':False,
        'max_msg_words'=70,
        'max_connection'=1,
    }
    

settings = {}
settings['honglian_01'] = {
    'name': 'honglian_01',
    'desc': 'honglian_01',
    
    'site': site_settings['honglian']
    'params':{
            'username':'jnfd',
            'password':'647185',
            'epid':'372',
    },
    'config': config_settings['honglian_001']
    
    'queue':{
        'request':'channel.request.honglian_01'
        'response':'channel.response.honglian_01'
        'error':'channel.response.channel_error'
        'log':'channel.log.honglian_01'
    }
}

settings['honglian_bjyh'] = {
    'name': 'honglian_bjyh',
    'desc': 'honglian_bjyh',
    
    'site': site_settings['honglian']

    'params':{
            'username':'jnfdbjyh',
            'password':'123456',
            'epid':'606',
    }
    'config': config_settings['honglian_001']

    'queue':{
        'request':'channel.request.honglian_bjyh'
        'response':'channel.response.honglian_bjyh'
        'error':'channel.response.channel_error'
        'log':'channel.log.honglian_bjyh'
    }

}

settings['honglian_jtyh'] = {
    'name': 'honglian_jtyh',
    'desc': 'honglian_jtyh',
    
    'site': site_settings['honglian']

    'params':{
            'username':'fdjtyh',
            'password':'123456',
            'epid':'607',
    }
    
    'config': config_settings['honglian_001']

    
    'queue':{
        'request':'channel.request.honglian_jtyh'
        'response':'channel.response.honglian_jtyh'
        'error':'channel.response.channel_error'
        'log':'channel.log.honglian_jtyh'
    }

}

settings['honglian_ty'] = {
    'name': 'honglian_ty',
    'desc': 'honglian_ty',
    
    'site': site_settings['honglian']
    'params':{
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
    }
    'config': config_settings['honglian_001']
    
    'queue':{
        'request':'channel.request.honglian_ty'
        'response':'channel.response.honglian_ty'
        'error':'channel.response.channel_error'
        'log':'channel.log.honglian_ty'
    }

}

settings['honglian_tyb'] = {
    'name': 'honglian_tyb',
    'desc': 'honglian_tyb',
    
    'site': site_settings['honglian']

    'params':{
            'username':'fdhz',
            'password':'123456',
            'epid':'6831',
    }
    'config': config_settings['honglian_001']
    'queue':{
        'request':'channel.request.honglian_tyb'
        'response':'channel.response.honglian_tyb'
        'error':'channel.response.channel_error'
        'log':'channel.log.honglian_tyb'
    }

}

settings['honglian_tyd'] = {
    'name': 'honglian_tyb',
    'desc': 'honglian_tyb',
    
    'site': site_settings['honglian']

    'params':{
            'username':'fdgg',
            'password':'123456',
            'epid':'6856',
    }
    'config': config_settings['honglian_001']
    'queue':{
        'request':'channel.request.honglian_tyd'
        'response':'channel.response.honglian_tyd'
        'error':'channel.response.channel_error'
        'log':'channel.log.honglian_tyd'
    }

}

settings['honglian_mock'] = {
    'name': 'honglian_mock',
    'desc': 'honglian_mock',
    
    'site': site_settings['honglian_mock']
    'params':{
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
    }
    'config': config_settings['honglian_001']
    'queue':{
        'request':'channel.request.honglian_mock'
        'response':'channel.response.honglian_mock'
        'error':'channel.response.channel_error'
        'log':'channel.log.honglian_mock'
    }

    
}
