'''
Created on 2011-10-18

@author: xbfool
'''
from process_ret_sd_ct import process_ret_sd_ct
from process_ret_changshang_a import process_ret_changshang_a, process_ret_106g, process_ret_106h, process_ret_106j, process_ret_106k, process_ret_106i
from process_ret_dongguan_0769 import process_ret_dongguan_0769
from process_ret_hb_ct import process_ret_hb_ct, process_ret_hb_ct_2
from process_ret_hlyd import process_ret_hlyd
from process_ret_honglian import process_ret_honglian
from process_ret_maoming_ct import process_ret_maoming_ct
from process_ret_scp_0591 import process_ret_scp_0591
from process_ret_shangxintong import *
from process_ret_zhangshangtong import *
from process_ret_cmpp import *
from process_req import *
import hashlib

from datetime import datetime
class sender_settings():
    def __init__(self):
        settings = {}
        settings['sd_ct_01'] = {
            'name': 'sd_ct_01',
            'host': '219.146.6.117',
            'path': '/AIS/HTTPService/SendSMS.aspx',
            'mode': 'POST',
            'sub_mode': 'sd_ct',
            'uid': '12345678901',
            'pwd': 'fd1234',
            'process_ret': process_ret_sd_ct,
            'process_req': process_req_sd_ct
        }
        settings['sd_ct_02'] = {
            'name': 'sd_ct_02',
            'host': '219.146.6.117',
            'path': '/AIS/HTTPService/SendSMS.aspx',
            'mode': 'POST',
            'sub_mode': 'sd_ct',
            'uid': 'lyzx',
            'pwd': '123456',
            'process_ret': process_ret_sd_ct,
            'process_req': process_req_sd_ct
        }
        settings['hb_ct_01'] = {
            'name': 'hb_ct_01', #0712a
            'host': '58.53.194.80',
            'path': '/swdx/services/APService',
            'mode': 'soap',
            'sub_mode':'hb_ct',
            'entid': 'hbalswdx4',
            'uid': 'hbalswdx402',
            'apid': 'hbalswdx402',
            'appwd': 'dufwe98r02q39',
            'process_ret' : process_ret_hb_ct,
            'process_req' : process_req_hb_ct
        }
        settings['hb_ct_02'] = {
            'name': 'hb_ct_02',
            'host': '58.53.194.80',
            'path': '/swdx/services/APService',
            'mode': 'soap',
            'sub_mode':'hb_ct',
            'entid': 'hbtmbckj',
            'uid': 'hbtmbckj3',
            'apid': 'hbtmbckj3',
            'appwd': '31Zup3FA',
            'process_ret' : process_ret_hb_ct,
            'process_req' : process_req_hb_ct
        }
        settings['hb_ct_03'] = {
            'name': 'hb_ct_03',
            'host': '58.53.194.80',
            'path': '/swdx/services/APService',
            'mode': 'soap',
            'sub_mode':'hb_ct',
            'entid': 'jzidcgs',
            'uid': 'jzidc2',
            'apid': 'jzidc2',
            'appwd': 'abcjzidc2',
            'process_ret' : process_ret_hb_ct,
            'process_req' : process_req_hb_ct
        }
        settings['hb_ct_04'] = {
            'name': 'hb_ct_04',
            'host': '58.53.194.80',
            'path': '/swdx/services/APService',
            'mode': 'soap',
            'sub_mode':'hb_ct',
            'entid': 'hbtmzx002',
            'uid': 'hbtmzx002',
            'apid': 'hbtmzx002',
            'appwd': 'Pb64Hct7',
            'webpwd': 'sdj5alk6',
            'process_ret' : process_ret_hb_ct,
            'process_req' : process_req_hb_ct
        }
        settings['hb_ct_05'] = {
            'name': 'hb_ct_05',
            'host': '58.53.194.80',
            'path': '/swdx/services/SmsBizService',
            'mode': 'soap',
            'sub_mode':'hb_ct_2',
            'entid': 'hbtmbckj',
            'uid': 'hbtmbckj',
            'apid': 'hbtmbckj',
            'appwd': 'b5EZq4BW',
            'webpwd': 'sdj5alk6',
            'process_ret' : process_ret_hb_ct_2,
            'process_req' : process_req_hb_ct_2
        }
        settings['hlyd_01'] = {
            'name': 'hlyd_01',
            'host': '58.83.147.85',
            'port': '8080',
            'path': '/qxt/smssenderv2',
            'mode': 'GET',
            'user': 'jnfd',
            'sub_mode': 'hlyd',
            'password': 'jnfd123',
            'process_ret' : process_ret_hlyd,
            'process_req' : process_req_hlyd
        }
        settings['changshang_a_01'] = {
            'name': 'changshang_a_01',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '101083',
            'corp_pwd': 'f101083',
            'corp_service':'10655lt',
            'process_ret' : process_ret_changshang_a,
            'process_req' : process_req_changshang_a
        }
        
        settings['changshang_a_02'] = {
            'name': 'changshang_a_02',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '10108301',
            'corp_pwd': 'f101083',
            'corp_service':'10659dx',
            'process_ret' : process_ret_changshang_a,
            'process_req' : process_req_changshang_a
        }
        
        settings['changshang_a_03'] = {
            'name': 'changshang_a_03',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '10108302',
            'corp_pwd': 'f101083',
            'corp_service':'0514yd',
            'process_ret' : process_ret_changshang_a,
            'process_req' : process_req_changshang_a
        }
        
        settings['changshang_a_04'] = {
            'name': 'changshang_a_04',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '10108304',
            'corp_pwd': 'f101083',
            'corp_service':'lthy',
            'process_ret' : process_ret_changshang_a,
            'process_req' : process_req_changshang_a
        }
        
        settings['honglian_01'] = {
            'name': 'honglian_01',
            'host': 'q.hl95.com',
            'path': '/',
            'mode': 'GET',
            'port': '8061',
            'sub_mode': 'honglian',
            'username':'jnfd',
            'password':'647185',
            'epid':'100372',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        
        settings['honglian_bjyh'] = {
            'name': 'honglian_bjyh',
            'host': 'q.hl95.com',
            'path': '/',
            'mode': 'GET',
            'port': '8061',
            'sub_mode': 'honglian',
            'username':'jnfdbjyh',
            'password':'123456',
            'epid':'100606',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        
        settings['honglian_jtyh'] = {
            'name': 'honglian_jtyh',
            'host': 'q.hl95.com',
            'path': '/',
            'mode': 'GET',
            'port': '8061',
            'sub_mode': 'honglian',
            'username':'fdjtyh',
            'password':'123456',
            'epid':'100607',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
                
        settings['honglian_ty'] = {
            'name': 'honglian_ty',
            'host': 'q.hl95.com',
            'path': '/',
            'mode': 'GET',
            'port': '8061',
            'sub_mode': 'honglian',
            'username':'fdzxyy',
            'password':'abc123',
            'epid':'106101',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        
        settings['honglian_tyb'] = {
            'name': 'honglian_tyb',
            'host': 'q.hl95.com',
            'path': '/',
            'mode': 'GET',
            'port': '8061',
            'sub_mode': 'honglian',
            'username':'fdhz',
            'password':'123456',
            'epid':'106831',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        settings['honglian_tyd'] = {
            'name': 'honglian_tyd',
            'host': 'q.hl95.com',
            'path': '/',
            'mode': 'GET',
            'port': '8061',
            'sub_mode': 'honglian',
            'username':'fdgg',
            'password':'123456',
            'epid':'106856',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        settings['shangxintong_01'] = {
            'name': 'shangxintong_01',
            'host': '218.15.25.98',
            'path': '/sxt_webservice/services/SMSService?wsdl',
            'mode': 'soap',
            'port': '8081',
            'sub_mode': 'shangxintong',
            'account': 'ykxx',
            'password': '123789',
            'process_ret' : process_ret_shangxintong,
            'process_req' : process_req_shangxintong
        }
        settings['maoming_ct_0668'] = {
            'name': 'maoming_ct_0668',
            'host': '113.107.163.203',
            'path': '/WebService1.6/sendSMS',
            'port': '8080',
            'sub_mode': 'maoming_ct',
            'srcmobile': 'fuda',
            'password': 'fudaduanxin123',
            'mode': 'POST',
            'process_ret': process_ret_maoming_ct,
            'process_req' : process_ret_maoming_ct
        }
        settings['scp_0591_a'] = {
            'name': 'scp_0591_a',
            'host': 'www.smsbird.cn',
            'path': '/UserInterface/SendSmsBatch.asp',
            'port': '8000',
            'sub_mode': 'scp_0591',
            'UserName': '90088',
            'Password': '123456',
            'mode': 'GET',
            'process_ret': process_ret_scp_0591,
            'process_req' : process_req_scp_0591
        }
        settings['card_send_a'] = {
            'name': 'card_send_a',
            'sub_mode': 'card_send',
            'mode': 'GET',
            'host': 'localhost',
            'path': '/',
            'port': '8000',
            'process_ret': None,
            'process_req' : None
        }
        settings['qixintong2012_01'] = {
            'name': 'qixintong2012_01',
            'host': '202.85.214.57',
            'path': '/service/sms/text/SendSms.ashx',
            'port': '8087',
            'sub_mode': 'qixintong2012',
            'uid': 'cjc106d',
            'pwd': '123456',
            'mode': 'POST',
            'process_ret': process_ret_qixintong2012,
            'process_req' : process_req_qixintong2012
        }
        settings['qixintong2012_02'] = {
            'name': 'qixintong2012_02',
            'host': '202.85.214.57',
            'path': '/service/sms/text/SendSms.ashx',
            'port': '8087',
            'sub_mode': 'qixintong2012',
            'uid': 'cjc106da',
            'pwd': '123456',
            'mode': 'POST',
            'process_ret': process_ret_qixintong2012,
            'process_req' : process_req_qixintong2012
        }

        #106e
        settings['zhangshangtong_01'] = {
            'name': 'zhangshangtong_01',
            'host': 'pi.f3.cn',
            'path': '/SendSMS.aspx',
            'port': '80',
            'sub_mode': 'zhangshangtong',
            'ececcid':'305990',
            'password':'fddx123',
            'msgtype':'5',
            'longcode':'111',
            'mode': 'POST',
            'process_ret': process_ret_zhangshangtong,
            'process_req' : process_req_zhangshangtong
        }

        #106ea
        settings['zhangshangtong_02'] = {
            'name': 'zhangshangtong_02',
            'host': 'pi.f3.cn',
            'path': '/SendSMS.aspx',
            'port': '80',
            'sub_mode': 'zhangshangtong',
            'ececcid':'305990001',
            'password':'jnfd123',
            'msgtype':'5',
            'longcode':'111',
            'mode': 'POST',
            'process_ret': process_ret_zhangshangtong,
            'process_req' : process_req_zhangshangtong
        }
        #106eb
        settings['zhangshangtong_03'] = {
            'name': 'zhangshangtong_03',
            'host': 'pi.f3.cn',
            'path': '/SendSMS.aspx',
            'port': '80',
            'sub_mode': 'zhangshangtong',
            'ececcid':'305990002',
            'password':'jtyh888',
            'msgtype':'5',
            'longcode':'111',
            'mode': 'POST',
            'process_ret': process_ret_zhangshangtong,
            'process_req' : process_req_zhangshangtong
        }
        settings['106f_95559'] = {
            'name': '106f_95559',
            'host': '221.179.180.158',
            'path': '/QxtSms/QxtFirewall',
            'port': '9002',
            'sub_mode': '106f',
            'OperID':'fuda',
            'OperPass':'72afw54e',
            'mode': 'GET',
            'process_ret': process_ret_106f,
            'process_req' : process_req_106f
        }

        settings['106f_95526'] = {
            'name': '106f_95526',
            'host': '221.179.180.158',
            'path': '/QxtSms/QxtFirewall',
            'port': '9002',
            'sub_mode': '106f',
            'OperID':'fuda1',
            'OperPass':'daf236w9',
            'mode': 'GET',
            'process_ret': process_ret_106f,
            'process_req' : process_req_106f
        }

        settings['cmpp_beijing_1'] = {
            'name': 'cmpp_beijing_1',
            'host': '127.0.0.1',
            'path': '/api/submitapi',
            'port': '7778',
            'sub_mode': 'cmpp_web',
            'username': 'fudaduanxin',
            'password': 'test1234',
            'mode': 'GET',
            'process_ret': process_ret_cmpp_web,
            'process_req': process_req_cmpp_web
        }

        settings['106g'] = {
            'name': '106g',
            'host': '112.2.36.53',
            'path': '/SendSms.asp',
            'port': '8091',
            'sub_mode': '106g',
            'account': 'jnfd8',
            'password': '123456789',
            'channel':'5',
            'mode': 'POST',
            'process_ret': process_ret_106g,
            'process_req': process_req_106g
        }

        settings['106ha'] = {
            'name': '106ha',
            'host': '115.29.177.224',
            'path': '/Service.asmx/sendsms',
            'port': '8089',
            'sub_mode': '106h',
            'zh': 'jnfd',
            'mm': 'M5d~6k9-]8h.5F[d2#1K',
            'dxlbid': '24',
            'mode': 'POST',
            'process_ret': process_ret_106h,
            'process_req': process_req_106ha
        }

        settings['106hb'] = {
            'name': '106hb',
            'host': '115.29.177.224',
            'path': '/Service.asmx/sendsms',
            'port': '8089',
            'sub_mode': '106h',
            'zh': 'fddxgg',
            'mm': 'Q58h.5F[k9-]d2d~6#1G',
            'dxlbid': '13',
            'mode': 'POST',
            'process_ret': process_ret_106h,
            'process_req': process_req_106hb
        }

        settings['106j'] = {
            'name': '106j',
            'host': 'www.qyqq.cn',
            'path': '/sms.aspx',
            'port': '8888',
            'sub_mode': '106j',
            'userid': '9944',
            'account': 'jnfd',
            'password': 'a123456',
            'mode': 'POST',
            'process_ret': process_ret_106j,
            'process_req': process_req_106j
        }

        settings['106k'] = {
            'name': '106k',
            'host': '211.147.239.62',
            'path': '/cgi-bin/sendsms?username=001@bjjnfd',
            'port': '9050',
            'sub_mode': '106k',
            'username': '001@bjjnfd',
            'password': '123456',
            'mode': '106K',
            'process_ret': process_ret_106k,
            'process_req': process_req_106k
        }

        settings['106i'] = {
            'name': '106i',
            'host': '42.96.248.183',
            'path': '/sendsms.php',
            'port': '8080',
            'sub_mode': '106i',
            'userid': '100565',
            'username': 'JNFDH',
            'password': 'CyfpI*l9',
            'mode': 'GET',
            'ext': '124',
            'process_ret': process_ret_106i,
            'process_req': process_req_106i
        }

        settings['default'] = settings['hb_ct_01']
        
        self.settings = settings
        for item in settings.itervalues():
            item['timeout_count'] = 0
            item['last_update'] = datetime.now()
