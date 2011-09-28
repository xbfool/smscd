# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from Queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
from time import sleep

from loadcfg import loadcfg
from dbsql import dbsql
from zhttp import zhttp_pool
from xml.dom.minidom import parseString
from xml.sax import saxutils
from message import message
from traceback import print_exc
from urlparse import urlparse
import urllib
import phonenumber
from struct import *
from hashlib import md5
from base64 import b64encode
from zlib import compress
from random import seed, shuffle
class sms_sender(object):
    def __init__(self, chk_interval=3):
        self.__chk_interval = chk_interval
        self.cfg = loadcfg('smsd.ini')
        
        settings = {}
        settings['sd_ct_01'] = {
            'name': 'sd_ct_01',
            'host': '219.146.6.117',
            'path': '/AIS/HTTPService/SendSMS.aspx',
            'mode': 'POST',
            'sub_mode': 'sd_ct',
            'uid': '12345678901',
            'pwd': 'fd1234',
            'process_ret': sms_sender.__process_ret_sd_tc
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
            'process_ret' : sms_sender.__process_ret_hb_tc
        }
        settings['hb_ct_02'] = {
            'name': 'hb_ct_02',
            'host': '58.53.194.80',
            'path': '/swdx/services/APService',
            'mode': 'soap',
            'sub_mode':'hb_ct',
            'entid': 'szsccp',
            'uid': 'sccp02',
            'apid': 'apszsccp02',
            'appwd': '7878779',
            'process_ret' : sms_sender.__process_ret_hb_tc
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
            'process_ret' : sms_sender.__process_ret_hb_tc
        }
#        settings['hb_ct_04'] = {
#            'name': 'hb_ct_04',
#            'host': '58.53.194.80',
#            'path': '/swdx/services/APService',
#            'mode': 'soap',
#            'sub_mode':'hb_ct',
#            'entid': 'hbtmbckj',
#            'uid': 'hbtmbckj4',
#            'apid': 'hbtmbckj4',
#            'appwd': '75Kfa8QL',
#            'webpwd': 'sdj5alk6',
#            'process_ret' : sms_sender.__process_ret_hb_tc
#        }
        settings['hb_ct_04'] = {
            'name': 'hb_ct_04',
            'host': '58.53.194.80',
            'path': '/swdx/services/APService',
            'mode': 'soap',
            'sub_mode':'hb_ct',
            'entid': 'hbtmbckj',
            'uid': 'hbtmbckj',
            'apid': 'hbtmbckj',
            'appwd': 'b5EZq4BW',
            'webpwd': 'sdj5alk6',
            'process_ret' : sms_sender.__process_ret_hb_tc
        }
        settings['hlyd_01'] = {
            'name': 'hlyd_01',
            'host': 'hl.my2my.cn',
            'path': '/services/esmsservice',
            'mode': 'soap',
            'sub_mode': 'hlyd',
            'cpid': '9033',
            'cppwd': '123456',
            'process_ret' : sms_sender.__process_ret_hlyd
        }
        settings['changshang_a_01'] = {
            'name': 'changshagn_a_01',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '101083',
            'corp_pwd': 'f101083',
            'corp_service':'10655lt',
            'process_ret' : sms_sender.__process_ret_changshang_a
        }
        
        settings['changshang_a_02'] = {
            'name': 'changshagn_a_02',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '10108301',
            'corp_pwd': 'f101083',
            'corp_service':'10659dx',
            'process_ret' : sms_sender.__process_ret_changshang_a
        }
        
        settings['changshang_a_03'] = {
            'name': 'changshagn_a_03',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '10108302',
            'corp_pwd': 'f101083',
            'corp_service':'0514yd',
            'process_ret' : sms_sender.__process_ret_changshang_a
        }
        
        settings['changshang_a_04'] = {
            'name': 'changshagn_a_04',
            'host': '123.196.114.68',
            'port': '8080',
            'path': '/sms_send2.do',
            'mode': 'POST',
            'sub_mode': 'changshang_a',
            'corp_id': '10108304',
            'corp_pwd': 'f101083',
            'corp_service':'lthy',
            'process_ret' : sms_sender.__process_ret_changshang_a
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
            'process_ret': sms_sender.__process_ret_honglian
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
            'process_ret': sms_sender.__process_ret_honglian
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
            'process_ret': sms_sender.__process_ret_honglian
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
            'process_ret': sms_sender.__process_ret_honglian
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
            'process_ret' : sms_sender.__process_ret_shangxintong
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
            'process_ret': sms_sender.__process_ret_maoming_ct
        }
        settings['scp_0591_a'] = {
            'name': 'scp_0591a',
            'host': 'www.smsbird.cn',
            'path': '/UserInterface/SendSmsBatch.asp',
            'port': '8000',
            'sub_mode': 'scp_0591',
            'UserName': '90088',
            'Password': '123456',
            'mode': 'GET',
            'process_ret': sms_sender.__process_ret_scp_0591
        }
#        settings['dongguan_0769_01'] = {
#            'name': 'dongguan_0769_01',
#            'host': '61.145.168.234',
#            'port': '90',
#            'path': '/Interface.asmx',
#            'mode': 'soap',
#            'sub_mode': 'dongguan_0769',
#            'UserName': '闪捷科技1',
#            'UserPwd': md5('123456').hexdigest(),
#            'process_ret' : sms_sender.__process_ret_dongguan_0769
#        }
        settings['default'] = settings['hb_ct_01']
        self.settings = settings
        self.__zhttp_pool = zhttp_pool(1, settings, self.__http_callback)
        
        self.__db = dbsql(**self.cfg.database.raw_dict)
        self.__dblock = Lock()
        
        self.__ret_queue = Queue(0x10000)
        
        self.__pending = []
        
        self.__worker_exit_lock = Lock()
        self.__worker_exit_lock.acquire()
        self.__worker_thread = Thread(None, self.__worker, '%s checker thread' % self.__class__.__name__)
        self.__worker_thread.start()
    
    def stop(self):
        self.__zhttp_pool.stop()
        self.__worker_exit_lock.release()
        self.__worker_thread.join()
    
    def __http_callback(self, param, ret):
        # CAUTION: must thread safe
        self.__ret_queue.put((param, ret))
    
    def __worker(self):
        while not self.__worker_exit_lock.acquire(False):
            now = datetime.now()
            # process returns
            self.__process_ret(now)
            # process pending queue from database
            if self.__process_queue() == 0:
                #print '%s: no pending queue, sleep for %d seconds' % (self.__class__.__name__, self.__chk_interval)
                sleep(self.__chk_interval)
          
    def __process_ret_sd_tc(self, param):
        print 'ret sd tc'
        status = message.F_FAIL
        success_str = "Information%3a%e6%b6%88%e6%81%af%e5%8f%91%e9%80%81%e6%88%90%e5%8a%9f%ef%bc%8c%e8%af%b7%e6%9f%a5%e7%9c%8b%e4%ba%92%e5%8a%a8%e4%bf%a1%e7%ae%b1%ef%bc%81%09"
        try:
            resultstr = param['ret'][2]
            result = urllib.unquote(resultstr)
        except:
            result = "something is error"
            pass
        if resultstr == success_str:
            status = message.F_SEND
            try:
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))
            except:
                pass
            
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass

        return 1

    def __process_ret_honglian(self, param):
        print 'ret honglian'
        status = message.F_FAIL
        success_str = "00"
        try:
            resultstr = param['ret'][2]
            result = urllib.unquote(resultstr)
            result = result.decode('gbk').encode('utf8')
        except:
            result = "something is error"
            print result
            
        if result == success_str:
            status = message.F_SEND
            try:
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))
                self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
  
            except:
                pass
        else:  
            try:
                self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                        (status, param['time'], result, 0, param['uid']))
                print "honglian send failed"
            except:
                pass

        return 1

    def __process_ret_hb_tc(self, param):
        status = message.F_FAIL
        result = ''
        try:
            resultDOM = parseString(param['ret'][2])
            result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.data
            print result
            
            if result == 'messageSuccess':
                status = message.F_SEND
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))
            elif result == 'not enough money!':
                status = message.F_FAIL
        except:
            pass
        
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass
        return 1  
    
    def __process_ret_hlyd(self, param):
        status = message.F_FAIL
        try:
            resultDOM = parseString(param['ret'][2])
            result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.data
        
        
            if result == '0':
                status = message.F_SEND
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))
        except:
            status = message.F_FAIL
            pass
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass
        return 1  
    
    
    def __process_ret_changshang_a(self, param):
        status = message.F_FAIL
        try:
            result = param['ret'][2] 
        
            if result[0] == '0':
                status = message.F_SEND
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))
        except:
            status = message.F_FAIL
            pass
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass
        return 1  
    
    def __process_ret_dongguan_0769(self, param):
        status = message.F_FAIL
        try:
            result = param['ret'][2] 
            
            if result[0] == '0':
                status = message.F_SEND
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))
        except:
            status = message.F_FAIL
            pass
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass
        return 1  
    
    def __process_ret_shangxintong(self, param):
        status = message.F_FAIL
        try:
            resultDOM = parseString(param['ret'][2])
            result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.nextSibling.firstChild.data

            print result
            if result[0] == '0':
                status = message.F_SEND
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))
        except:
            status = message.F_FAIL
            pass
        try:
             self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass
        return 1  
    
    def __process_ret_maoming_ct(self, param):
        status = message.F_FAIL
        try:
            result = param['ret'][2]
            if result == '0\r\n':
                status = message.F_SEND
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))      
        except:
            status = message.F_FAIL
            pass
        
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass
        return 1  
    
    def __process_ret_scp_0591(self, param):
        status = message.F_FAIL
        rl = []
        try:
            result = param['ret'][2]
            print result
            rl = result.split(';')
            if rl[0].split('=')[1] == '0':
                status = message.F_SEND
                self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                            (param['msg_num'], param['user_uid']))      
        except:
            status = message.F_FAIL
            pass
        
        if len(rl) == 2:
            try:
                result = rl[1].split('=')[1].decode('gbk').encode('utf8')
            except:
                pass
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
        except:
            pass
        return 1  
    def __process_ret(self, now):
        count = 0
        while True:
            try:
                param, ret = self.__ret_queue.get(False)
            except Empty:
                # print '%s: no response yet' % self.__class__.__name__
                break
            print '%d, %s' % (param['uid'], ret)
            try:
                self.__pending.remove(param['uid'])
            except:
                print '%s: CAUTION, uid %d does NOT exist in __pending' \
                % (self.__class__.__name__, param['uid'])
                
            try:
                if param['setting'] != None and param['setting'].get('process_ret'):
                    process = param['setting']['process_ret']
                    param['time'] = now
                    param['ret'] = ret
                    count = count + process(self, param)
            except:
                pass
                
        if count > 0:
            self.__db.raw_commit()
    
    def get_filtered_addr(self, addr, percent, my_seed):
        addr.sort()
        seed(my_seed)
        shuffle(addr)
        
        ret = addr[0:max(1, len(addr) * percent / 100)]
        return ret
        
    def __process_queue(self):
        q = self.__db.raw_sql_query('SELECT user_uid, uid,address,msg,channel, msg_num, totaL_num, seed FROM message WHERE status = %s and channel != "send_card_a" ORDER BY uid DESC LIMIT 500',
                                     message.F_ADMIT)
        count = 0
        for user_uid, uid, address, msg, channel, msg_num, total_num, my_seed in q:
            if uid in self.__pending:
                continue
            user_content = self.__db.raw_sql_query('SELECT ext FROM user WHERE uid = %s', user_uid)
            ext = user_content[0][0]
            user_percent = self.__db.raw_sql_query('SELECT percent FROM user WHERE uid = %s', user_uid)
            percent = user_percent[0][0]
            if percent == None or percent > 100:
                percent = 100
                
            address_list = address.split(';')
            if(percent is not None and percent <= 100 and percent >= 50 and total_num >= 100):
                address_list = self.get_filtered_addr(address.split(';'), percent, my_seed)
            print "seed: ", my_seed
            print "addr_list:", address_list

            # get channel according to user channel info
            pm = phonenumber.phonenumber()
            channel_type = pm.check_addr(address_list[0])
            if channel_type == pm.S_CM:
                user_channel = self.__db.raw_sql_query('SELECT channel_cm FROM user WHERE uid = %s', user_uid)
            elif channel_type == pm.S_CU:
                user_channel = self.__db.raw_sql_query('SELECT channel_cu FROM user WHERE uid = %s', user_uid)
            elif channel_type == pm.S_CT:
                user_channel = self.__db.raw_sql_query('SELECT channel_ct FROM user WHERE uid = %s', user_uid)
            channel = user_channel[0][0]

            addr = ','.join(address_list)
            #for addr in address_list:
            self.__pending.append(uid)
            if channel == None or not self.settings.get(channel):
                channel = 'default'
                
            if channel != None and self.settings.get(channel):
                setting = self.settings.get(channel) 
                try:
                    msg = saxutils.escape(msg).encode('UTF-8')
                except:
                    try:
                        msg = saxutils.escape(msg)
                    except:
                        print_exc()

                try:
                    parseString('<xml>%s</xml>' % msg)
                except:
                    print_exc()
                if setting.get('sub_mode') == 'hb_ct':
                    print "in hb_ct..."
                    soap = \
'''
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <SendMessage xmlns="http://trust.me.nobody/cares/this/">
            <ApName>%s</ApName>
            <ApPassword>%s</ApPassword>
            <compcode>%s</compcode>
            <userCode>%s</userCode>
            <calledNumber>%s</calledNumber>
            <sendTime>%s</sendTime>
            <content>%s</content>
        </SendMessage>
    </soap:Body>
</soap:Envelope>
''' \
                    % (setting['apid'], setting['appwd'], setting['entid'], setting['uid'],
                       addr, '', msg)
                    print setting['name']
                    
                    self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                      soapaction='http://58.53.194.80/swdx/services/APService/',
                                      soap=soap)
                    # self.__zhttp_pool.req('hb', uid, address = address, content = msg)
                    count += 1
                elif setting.get('sub_mode') == 'sd_ct':
                    print "in sd_ct.."
                    address_f = [address_list[i] for i in range(len(address_list)) if address_list[i][0:3] != '182']
                    if len(address_f) > 0:
                        self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                              address=';'.join(address_f), content=msg, uid='12345678901',
                                            pwd='fd1234')
                    else:
                        self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                              address=';'.join(address_list), content=msg, uid='12345678901',
                                            pwd='fd1234')
                    count += 1
                    
                elif setting.get('sub_mode') == 'honglian':
                    print "in honglian.."
                    self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                          phone=addr, message=msg.decode('utf8').encode('gbk'),
                                          username=setting['username'],
                                          password=setting['password'], epid=setting['epid'],
                                          subcode=ext,
                                        )
                    count += 1
                elif setting.get('sub_mode') == 'hlyd':
                    print "in hlyd..."
                    soap = \
'''
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <sendSmsAsNormal xmlns="http://trust.me.nobody/cares/this/">
            <phone>%s</phone>
            <msgcont>%s</msgcont>
            <spnumber>%s</spnumber>
            <chid>%s</chid>
            <cpid>%s</cpid>
            <cppwd>%s</cppwd>
        </sendSmsAsNormal>
    </soap:Body>
</soap:Envelope>
''' \
                    % (addr, msg, '', '',
                       setting['cpid'], setting['cppwd'])
                    self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                      soapaction='http://hl.my2my.cn/services/esmsservice',
                                      soap=soap)   
                    count += 1
                    
                elif setting.get('sub_mode') == 'shangxintong':
                    print "in shangxintong ..."
                    soap = \
'''
<SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://message.scape.gsta.com" xmlns:mul="http://www.muleumo.org" xmlns:sms="http://sms.cap.scape.gsta.com" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP:Header xmlns:Header="Header"/>
    <SOAP:Body>
        <mul:sendSMS>
        <mul:in0>
        <mes:account>%s</mes:account>
        <mes:extendField/>
        <mes:hashCode/>
        <mes:password>%s</mes:password>
        <mes:timestamp/>
        </mul:in0>
        <mul:in1>
        <mes:account/>
        <mes:id/>
        </mul:in1>
        <mul:in2>
        <sms:content>%s</sms:content>
        <sms:contentFormat>1</sms:contentFormat>
        <sms:needFeedback>1</sms:needFeedback>
        <sms:password/><sms:receivers>
        <mul:string>%s</mul:string>
        </sms:receivers><sms:areacode/>
        <sms:sender/>
        </mul:in2>
        </mul:sendSMS>
    </SOAP:Body>
</SOAP:Envelope>
'''\
                    % (setting['account'],
                       setting['password'],
                       msg,
                       addr)
                    
                    self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                      soapaction='sendSMS',
                                      soap=soap, port=8081)   
                    count += 1
                elif setting.get('sub_mode') == 'changshang_a':
                    print "in changshang_a"
                    tmpmsg = unicode(msg, 'utf-8')
                    sendmsg = msg
	            try:
                        sendmsg = tmpmsg.encode('gbk')
                    except:
                        pass
                    if ext == None or ext == '':  
                        self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                              corp_id=setting['corp_id'], corp_pwd=setting['corp_pwd'], corp_service=setting['corp_service'],
                                              mobile=addr, msg_content=sendmsg)
                    else:
                        self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                              corp_id=setting['corp_id'], corp_pwd=setting['corp_pwd'], corp_service=setting['corp_service'], ext=ext,
                                              mobile=addr, msg_content=sendmsg)
                    count += 1
                    
                elif setting.get('sub_mode') == 'dongguan_0769':
                    print "in dongguan_9769..."
                    msgtext = \
'''
<Ms c=\"1\">
  <m>
    <FA/>
    <FD>%s</FD>
    <FM>%s</FM>
    <FT/>
    <NR/>
</Ms>
''' \
                    % (addr, msg)
                    
                    soap = \
'''
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <Sms_SendEx2 xmlns="http://tempuri.org/">
      <CompCode></CompCode>
      <UserName>%s</UserName>
      <UserPwd>%s</UserPwd>
      <SendMsgXML>%s</SendMsgXML>
      <withfollow>%s</withfollow>
    </Sms_SendEx>
  </soap:Body>
</soap:Envelope>
''' \
                    % (setting['UserName'], setting['UserPwd'], b64encode(compress(msgtext)), 0)
                    self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                                      soapaction='http://61.145.168.234:90/Interface.asmx',
                                      soap=soap)   
                    count += 1
                elif setting.get('sub_mode') == 'maoming_ct':
                    print "in maoming_ct"
                    tmpmsg = unicode(msg, 'utf-8')
                    self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                      srcmobile=setting['srcmobile'], password=setting['password'],
                      objmobiles=addr, smstext=tmpmsg.encode('gbk'), rstype='text')
                elif setting.get('sub_mode') == 'scp_0591':
                    print "in scp_0591"
                    address_shu = '|'.join(address.split(';'))
                    tmpmsg = unicode(msg, 'utf-8')
                    self.__zhttp_pool.req(channel, {'user_uid':user_uid, 'setting':setting, 'uid':uid, 'msg_num':msg_num, 'percent':percent},
                      Mobile=address_shu, MsgContent=tmpmsg.encode('gbk'))
        return count
                    

if __name__ == '__main__':
    sender = sms_sender()
    
    #from os import system
    #system('pause')
    
    import time
    while True:
        time.sleep(10)
    sender.stop()
