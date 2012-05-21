#!/usr/bin/env python
# -*- coding: utf-8 -*-
site_settings = {}

site_settings['honglian'] = {
    'host': '219.238.160.81',
    'path': '/interface/limitnew.asp',
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
            'username':'fdgg',
            'password':'123456',
            'epid':'6856',
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

settings['changshang_a_01'] = {
    'name': 'changshang_a_01',
    'desc': '联通106a',
    
    'site': site_settings['changshang_a'],
    'params':{
            'corp_id': '101083',
            'corp_pwd': 'f101083',
            'corp_service':'10655lt'
    },
    'config': config_settings['changshang_a_001'],
    'support': support_settings['cu'],
    'queue':{
        'request':'channel.request.changshang_a_01',
        'response':'channel.response.changshang_a_01',
        'error':'channel.response.channel_error',
        'log':'channel.log.changshang_a_01',
    }
}


settings['changshang_a_02'] = {
    'name': 'changshang_a_02',
    'desc': '电信106a',
    
    'site': site_settings['changshang_a'],
    'params':{
            'corp_id': '10108301',
            'corp_pwd': 'f101083',
            'corp_service':'10659dx',
    },
    'config': config_settings['changshang_a_001'],
    'support': support_settings['ct'],
    'queue':{
        'request':'channel.request.changshang_a_02',
        'response':'channel.response.changshang_a_02',
        'error':'channel.response.channel_error',
        'log':'channel.log.changshang_a_02',
    }
}

settings['changshang_a_03'] = {
    'name': 'changshang_a_03',
    'desc': '移动106a',
    
    'site': site_settings['changshang_a'],
    'params':{
            'corp_id': '10108302',
            'corp_pwd': 'f101083',
            'corp_service':'0514yd',
    },
    'config': config_settings['changshang_a_001'],
    'support': support_settings['cm'],
    'queue':{
        'request':'channel.request.changshang_a_03',
        'response':'channel.response.changshang_a_03',
        'error':'channel.response.channel_error',
        'log':'channel.log.changshang_a_03',
    }
}

settings['changshang_a_04'] = {
    'name': 'changshang_a_04',
    'desc': '联通106a',
    
    'site': site_settings['changshang_a'],
    'params':{
            'corp_id': '10108304',
            'corp_pwd': 'f101083',
            'corp_service':'lthy',
    },
    'config': config_settings['changshang_a_001'],
    'support': support_settings['cu'],
    'queue':{
        'request':'channel.request.changshang_a_04',
        'response':'channel.response.changshang_a_04',
        'error':'channel.response.channel_error',
        'log':'channel.log.changshang_a_04',
    }
}

settings['changshang_a_04'] = {
    'name': 'changshang_a_04',
    'desc': '联通106a',
    
    'site': site_settings['changshang_a'],
    'params':{
            'corp_id': '10108304',
            'corp_pwd': 'f101083',
            'corp_service':'lthy',
    },
    'config': config_settings['changshang_a_001'],
    'support': support_settings['cu'],
    'queue':{
        'request':'channel.request.changshang_a_04',
        'response':'channel.response.changshang_a_04',
        'error':'channel.response.channel_error',
        'log':'channel.log.changshang_a_04',
    }
}

settings['qixintong2012_106d_01'] = {
    'name': 'qixintong2012_106d_01',
    'desc': '联通106d_91',
    
    'site': site_settings['qixintong2012_106d'],
    'params':{
            'ua': 'sdcjc',
            'pw': '318340',
    },
    'config': config_settings['qixintong2012_106d_001'],
    'support': support_settings['all'],
    'queue':{
        'request':'channel.request.qixintong2012_106d_01',
        'response':'channel.response.qixintong2012_106d_01',
        'error':'channel.response.channel_error',
        'log':'channel.log.qixintong2012_106d_01',
    }
}





