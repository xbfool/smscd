# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from Queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
from time import sleep


from zhttp import zhttp_pool
from xml.dom.minidom import parseString
from xml.sax import saxutils

from traceback import print_exc
import phonenumber
from base64 import b64encode
from zlib import compress
from random import seed, shuffle
from settings import sender_settings
from ChannelController import ChannelController
from msg_util import *
class sms_sender(object):
    def __init__(self, chk_interval=3):
        self.__chk_interval = chk_interval
        self.channel_controller = ChannelController()
        self.msg_controller = MsgController()
        self.settings = sender_settings().settings
        for item in self.settings.itervalues():
            item['timeout_count'] = 0
            item['last_update'] = datetime.now()
        
        self.__zhttp_pool = zhttp_pool(1, self.settings, self.__http_callback, timeout_callback=self.__timeout_callback)
        

        self.__ret_queue = Queue(0x10000)
        
        self.__pending = []
        self.timeout_time = 1800
        self.__timeout_lock = Lock()
        self.__worker_exit_lock = Lock()
        self.__worker_exit_lock.acquire()
        self.__worker_thread = Thread(None, self.__worker, '%s checker thread' % self.__class__.__name__)
        self.__worker_thread.start()

    def stop(self):
        self.__zhttp_pool.stop()
        self.__worker_exit_lock.release()
        self.__worker_thread.join()
    
    def __timeout_add(self, setting):
        self.__timeout_lock.acquire()
        setting['timeout_count'] += 1
        setting['last_update'] = datetime.now()
        self.__timeout_lock.release()
        
    def __check_channel_ok(self, setting):
        if setting['timeout_count'] <= 3:
            return True
        elif (datetime.now() - setting['last_update']).total_seconds() > self.timeout_time:
            self.__timeout_clean(setting)
            return True
        else:
            return False
    def __timeout_clean(self, setting):
        self.__timeout_lock.acquire()
        setting['timeout_count'] = 0
        setting['last_update'] = datetime.now()
        self.__timeout_lock.release()
        
    def __http_callback(self, param, ret):
        # CAUTION: must thread safe
        self.__ret_queue.put((param, ret))
    def __timeout_callback(self, param, ret):
        self.__timeout_add(param['setting'])
        
    def __worker(self):
        while not self.__worker_exit_lock.acquire(False):
            now = datetime.now()
            # process returns
            self.__process_ret(now)
            # process pending queue from database
            if self.__process_queue_new() == 0:
                #print '%s: no pending queue, sleep for %d seconds' % (self.__class__.__name__, self.__chk_interval)
                sleep(self.__chk_interval)
    

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
                    self.__timeout_clean(param['setting'])
                    count = count + process(self, param)
            except:
                pass
                
        if count > 0:
            self.__db.raw_commit()
    
    def get_filtered_addr(self, addr, percent, my_seed, total_num=0):
        if(percent is not None and percent <= 100 and percent >= 50 and total_num >= 100):
            addr.sort()
            seed(my_seed)
            shuffle(addr)
            
            ret = addr[0:max(1, len(addr) * percent / 100)]
            return ret
        else:
            return addr
        
    def __process_queue_new(self):
        messages = self.msg_controller.get_messages()
        count = 0
        for msg in messages:
            if msg['uid'] in self.__pending:
                print self.__pending
                continue
            self.__pending.append(msg['uid'])
            
            msg['addr'] = msg['address'].split(';')
            #processor = self.channel_controller.get_processor(msg)
            #processor.send(msg)
            self.get_filtered_addr(msg['address'].split(';'), msg['percent'], msg['seed'], msg['total_num'])
            print msg
            
            count += 1
        return count

    def __process_queue(self):
        q = self.__db.raw_sql_query('SELECT user_uid, uid,address,msg,channel, msg_num, total_num, seed FROM message WHERE status = %s and channel != "card_send_a" ORDER BY uid DESC LIMIT 500',
                                     msg_status.F_ADMIT)
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
                if not self.__check_channel_ok(setting):
                    continue               
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
    
    import time
    while True:
        time.sleep(10)
    sender.stop()
