'''
Created on 2011-10-18

@author: xbfool
'''
from process_ret_sd_ct import process_ret_sd_ct
from process_ret_changshang_a import process_ret_changshang_a
from process_ret_dongguan_0769 import process_ret_dongguan_0769
from process_ret_hb_ct import process_ret_hb_ct, process_ret_hb_ct_2
from process_ret_hlyd import process_ret_hlyd
from process_ret_honglian import process_ret_honglian
from process_ret_maoming_ct import process_ret_maoming_ct
from process_ret_scp_0591 import process_ret_scp_0591
from process_ret_shangxintong import process_ret_shangxintong, process_ret_qixintong2012
from process_req import *
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
            'host': 'hl.my2my.cn',
            'path': '/services/esmsservice',
            'mode': 'soap',
            'sub_mode': 'hlyd',
            'cpid': '9033',
            'cppwd': '123456',
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
            'host': '219.238.160.81',
            'path': '/interface/limitnew.asp',
            'mode': 'POST',
            'sub_mode': 'honglian',
            'username':'jnfd',
            'password':'647185',
            'epid':'372',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        
        settings['honglian_bjyh'] = {
            'name': 'honglian_bjyh',
            'host': '219.238.160.81',
            'path': '/interface/limitnew.asp',
            'mode': 'POST',
            'sub_mode': 'honglian',
            'username':'jnfdbjyh',
            'password':'123456',
            'epid':'606',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        
        settings['honglian_jtyh'] = {
            'name': 'honglian_jtyh',
            'host': '219.238.160.81',
            'path': '/interface/limitnew.asp',
            'mode': 'POST',
            'sub_mode': 'honglian',
            'username':'fdjtyh',
            'password':'123456',
            'epid':'607',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
                
        settings['honglian_ty'] = {
            'name': 'honglian_ty',
            'host': '219.238.160.81',
            'path': '/interface/limitnew.asp',
            'mode': 'POST',
            'sub_mode': 'honglian',
            'username':'fdzxyy',
            'password':'123456',
            'epid':'6101',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        
        settings['honglian_tyb'] = {
            'name': 'honglian_tyb',
            'host': '219.238.160.81',
            'path': '/interface/limitnew.asp',
            'mode': 'POST',
            'sub_mode': 'honglian',
            'username':'fdhz',
            'password':'123456',
            'epid':'6831',
            'process_ret': process_ret_honglian,
            'process_req': process_req_honglian,
        }
        settings['honglian_tyd'] = {
            'name': 'honglian_tyd',
            'host': '219.238.160.81',
            'path': '/interface/limitnew.asp',
            'mode': 'POST',
            'sub_mode': 'honglian',
            'username':'fdgg',
            'password':'123456',
            'epid':'6856',
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
            'host': '202.85.221.191',
            'path': '/mc/httpsendsms.php',
            'port': '80',
            'sub_mode': 'qixintong2012',
            'ua': 'cjcsd',
            'pw': '1234',
            'mode': 'GET',
            'process_ret': process_ret_qixintong2012,
            'process_req' : process_req_qixintong2012
        }
        settings['qixintong2012_02'] = {
            'name': 'qixintong2012_02',
            'host': '202.85.221.191',
            'path': '/mc/httpsendsms.php',
            'port': '80',
            'sub_mode': 'qixintong2012',
            'ua': 'sdcjc',
            'pw': '318340',
            'mode': 'GET',
            'process_ret': process_ret_qixintong2012,
            'process_req' : process_req_qixintong2012
        }
        
        settings['default'] = settings['hb_ct_01']
        
        self.settings = settings
        for item in settings.itervalues():
            item['timeout_count'] = 0
            item['last_update'] = datetime.now()
