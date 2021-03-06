# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import sys
import re
print sys.path
from hashlib import sha1
from datetime import datetime, timedelta
import time
from traceback import print_exc,format_exc
import json

from utils import *

from loadcfg import loadcfg
from dbsql import dbsql
from dbobj import dbobj
from user import user
from message import message
import phonenumber
from phonebook import phonebook
from phone import phone
from addresslist import addresslist
from special_channel import *
from random import randint, seed
import sys
import os

from common.log import initLogger
from common.timer import Timer

#init logger
smsd_log_path = os.path.dirname(__file__) + "/log/"
logger = initLogger("smsd", smsd_log_path)

if __name__ != '__main__':
    smsd_path = os.path.dirname(__file__)
    sys.path.append(smsd_path)

        
class session(object):
    def __init__(self, user, active):
        self.user = user
        self.active = active # last activity of this session
        sid = sha1(user.username)
        sid.update(user.password)
        sid.update(str(active))
        self.sid = sid.hexdigest()
        self.username = user.username

        
    def check_active(self, timeout, now):
        if self.active + timeout < now:
            # session timeout
            return False
        else:
            self.active = now # also update
            return True

class log(object):
    def __init__(self, username, query, ret, datetime):
        self.username = username
        self.query = query
        self.ret = ret
        self.datetime = datetime
    
    def to_json(self):
        d = {}
        d['username'] = self.username
        d['query'] = self.query['q']
        d['errno'] = str(self.ret)
        d['datetime'] = self.datetime.isoformat(' ')
        return d
    
    
class smsd(object):
    PHONE_NUMBER = 1
    PHONE_NAME = 2
    
    def __init__(self, conf='smsd.ini', using_wsgiref=False):
        # get config/database, etc
        self.num_req = 0
        
        self.cfg = loadcfg(conf)
        
        self.db = dbsql(**self.cfg.database.raw_dict)
        
        self.__common_key = sha1('Shine bright morning light').hexdigest()
        
        self.__session_expire = self.cfg.smsd.session_expire
        
        self.users = {}
        self.user_ids = {}
        self.logs = []
        self.messages = {}
        self.commit_start_id = 0
        
        self.__reload_all()
        
        self.sessions = {}

        
        print 'smsd init complete'
    
    def __reload_all(self):
        logger.debug("__reload_all")
        
        user.set_db(self.db, 'user')
        message.set_db(self.db, 'message')
        users = user.load()
        
         
        if len(users) == 0:
            # add default user
            logger.debug('no user(s) found, creating default root user')
            u = user()
            u.new('root', 'root', sha1('debug').hexdigest(), 0, 1000, True,
                  False, True, 'default', 'default', 'default', user.F_CHARGE | user.F_CREATE_USER | user.F_CREATE_CHARGE)
            users = user.load()  
          
        for u in users:
            self.__add_user(u)
        
        tmp_users = {}
        for u in users:
            tmp_users[u.uid] = u
        for i in tmp_users.itervalues():
            if tmp_users.get(i.parent_id):
                tmp_users[i.parent_id].add_child(i)
                
        for u in users:
            self.user_ids[u.uid] = u
        logger.debug("Load User Cnt : %d " % len(users))    
            

    def reload_message(self, where = None):
        
        messages = message.load(where)
                #compute commit nums
        for m in messages:
            self.messages[m.uid] = m
            if m.last_update == None:
                m.last_update = m.create_time
                m.save('last_update')
            try:
                m.msg.decode('utf8')
            except:
                #print m.uid, 'cannot decode as utf8\n'
                try:
                    m.msg.decode('gbk')
                except:
                    print m.uid, 'cannot decode as gbk\n'
        logger.debug('load message count: %d' % len(messages))
        
    def __call__(self, env, start_response):
        # request handler hub
        self.num_req += 1
        if env['REQUEST_METHOD'] != 'POST' or 'CONTENT_LENGTH' not in env:
            logger.error('invalid query, not POST or invalid POST length')
            return self.__not_found(env, start_response)
        
        length = int(env['CONTENT_LENGTH'])
        
        if length <= 0:
            logger.error('invalid query, empty POST body')
            return self.__not_found(env, start_response)
        
        try:
            post_data = env['wsgi.input'].read(length)
            print post_data
        except:
            logger.error('error reading POST data')
            logger.error(format_exc())
            return self.__not_found(env, start_response)
        
        try:
            query = rec_uni2str(json.loads(post_data))
        except:
            logger.error('error parsing query: %s' % post_data)
            logger.error(format_exc())
            return self.__not_found(env, start_response)
        
        if 'q' not in query:
            logger.error('invalid query, no query key: %s' % post_data)
            return self.__not_found(env, start_response)
        
        q = query['q']
        self.__reload_all()
        if q == 'auth':
            # authenticate
            timer = Timer()
            session = self.__auth(query)
            if session == False:
                # auth failed
                self.__log_query_stat(query['user'], query, 1, timer.elapse())
                return self.__ret_json({'rtype':'err', 'errno':'1'}, start_response)
            
            self.db.raw_sql('INSERT INTO sessions(username,sid,active) VALUES(%s,%s,%s)',
                            (session.username, session.sid, session.active))
            
            self.__log_query_stat(session.username, query, 0, timer.elapse())
            return self.__ret_json({'rtype':'auth', 'sid':session.sid, 'username':session.username}, start_response)
        elif 'sid' in query:
            # check session
            timer = Timer()
            session = self.__chk_session(query['sid'])
            
            if session == False:
                # invalid/expired session
                self.__log_query_stat("", query, 2, timer.elapse())
                return self.__ret_json({'rtype':'err', 'errno':'2'}, start_response)
            
            
            try:
                processor = self.__getattribute__('processor_' + q)
            except:
                logger.error('invalid query, no suitable processor found for query \'%s\'' % q)
                logger.error(format_exc())
                return self.__not_found(env, start_response)
            
            try:
                errno, ret = processor(session.user, query)
                self.__log_query_stat(session.username, query, errno, timer.elapse())
            except:
                logger.error('exception raised while processing query \'%s\'' % q)
                logger.error(format_exc())
                self.__log_query_stat(session.username, query, 3, timer.elapse())
                return self.__ret_json({'rtype':'err', 'errno':'3'}, start_response)
            
            if errno != 0:
                # user defined error number, start from 0x0100
                return self.__ret_json({'rtype':'err', 'errno':errno, 'errmsg':ret}, start_response)
            
            return self.__ret_json(ret, start_response)
        else:
            logger.error('invalid query: %s' % post_data)
            return self.__not_found(env, start_response)
    
    def __not_found(self, env, start_response):
        start_response('404 NOT FOUND', [('Content-type', 'text/plain')])
        return ['Not Found']
    
    def __ret_json(self, ret, start_response):
        start_response('200 OK', [('Content-type', 'application/json')])
        return [json.dumps(ret, separators=(',', ':'))]
    
    def __add_user(self, u):
        self.users[u.username] = u
        self.user_ids[u.uid] = u
    
    def __auth(self, query):
        if 'user' not in query or 'pass' not in query:
            return False
        u = query['user'] # u for username
        p = query['pass'] # p for password
        logger.debug("__auth: user:%s | pass:%s " % (u,p))

        user = self.users.get(u)

        if not user:
            return False
        if not user.web_auth(p):
            return False
        s = session(user, time.time())

        self.sessions[s.sid] = s
        return s

    def __chk_session(self, session_id):
        logger.debug("__chk_session: %s" % session_id)
        ret = self.db.raw_sql_query('SELECT sid, username, active FROM sessions WHERE sid = %s AND active > %s',
                                   (session_id, time.time() - self.__session_expire))
        if len(ret) == 0:
            return None
        else:       
            sid, username, active = ret[0]
            user = self.users[username]
            s = session(user, active)
            self.db.raw_sql_query('UPDATE sessions SET active = %s where sid = %s',
                                   (time.time(), sid))
            return s
        
    def __chk_session_old(self, session_id):
        if session_id not in self.sessions:
            return False
        s = self.sessions[session_id]
        if not s.check_active(self.__session_expire, datetime.now()):
            del self.sessions[session_id]
            return False
        else:
            return s
    
    def __log_query_stat(self, username, query, errno, time):
        logger.info("Username:%s | Query:%s | Errorno:%d | ElapseTime:%dms" % (username, query, errno, time))
        
    def processor_echo(self, user, query):
        # example processor
        query['rtype'] = 'echo'
        return 0, query
    
    def processor_changepwd(self, u, query):
        #{'q':'changepwd', 'sid':sid, 'user':username, 'oldp':oldpassword, 'newp':newpassword}
        #TODO
        username = query['user']
        newp = query['newp']
        
        logger.debug("processor_changepwd | user:%s | newp:%s " % (username, newp))
        if not self.users.get(username):
            return False
        
        pu = self.users[username]
        if(not u.flags & user.F_CREATE_USER and pu.parent_id != u.uid) and pu.uid != u.uid:
            return False
        
        if pu.uid == u.uid:
            oldp = query['oldp']
            if not pu.web_auth(oldp):
                return 0, {'rtype':'changepwd', 'errno': 1};#密码错误
        
        pu.change_password(newp); 
        return 0, {'rtype':'changepwd', 'errno':0}#成功
    
    def processor_adduser(self, u, query):
        #{'q':'adduser', 'sid': sid, 'user':username, 'name':desc, 'pass':password, 'flags':flags,
        #'can_weblogin':can_weblogin, 'can_post':can_post, 'need_check';need_check}
        #TODO
        
        username = query['user']
        p = query['pass']
        flags = query['flags']
        desc = query['name']
        can_weblogin = query['can_weblogin']
        can_post = query['can_post']
        need_check = query['need_check']
        cm = query['cm']
        cu = query['cu']
        ct = query['ct']
        logger.debug("processor_adduser | username:%s | pass:%s | flags:%d | \
        desc:%s | can_weblogin:%d | can_post:%d | need_check:%d | cm:%s | cu:%s | ct:%s" % \
        (username, p, flags, desc, can_weblogin, can_post, need_check, cm, cu, ct))
        if not (u.flags & user.F_CREATE_USER):
            return False
        
        if flags & user.F_CHARGE or flags & user.F_CREATE_USER:
            if not (u.flags & user.F_CREATE_USER):
                return False
        
        if flags & user.F_CREATE_CHARGE:
            if u.username != 'root':
                return False
        
        if self.users.get(username):
            return 0, {'rtype':'adduser', 'errno' : 1} #重复用户
        
        new_user = user()
        new_user.new(username, desc, p, u.uid, 0, can_weblogin, can_post, need_check, cm, cu, ct, flags)
        new_user.percent = u.percent
        new_user.save()
        self.__add_user(new_user)
        u.add_child(new_user)
        
        return 0, {'rtype':'adduser', 'errno' : 0} #成功

    def processor_addmessage(self, u, query):
        #{'q':'addmessage, 'sid':sid, 'user':username, 'num':message_number}
        #TODO
        username = query['user']
        num = query['num']
        
        #root addmessage for itself
        if u.is_admin() and u.username == username:
            if u.msg_num + num >= 0:
                before_num = u.msg_num
                u.add_message(num)
                try:
                    self.db.raw_sql('INSERT INTO addmsglog(username,before_msg_num,add_msg_num,after_msg_num,type,create_time) VALUES(%s,%s,%s,%s,%s,%s)',
                        (u.username, before_num, num, u.msg_num, 0, datetime.now()))
                    logger.debug("processor_addmessage | username:%s | before_msg_num:%d | add_msg_num:%d | after_msg_num:%d | type:0"  
                                 % (u.username, before_num, num, u.msg_num))
                except:
                    pass
                return 0, {'rtype':'addmessage', 'num':num, 'errno': 0}
            else:
                return 0, {'rtype':'addmessage', 'num':num, 'errno':-1} #cannot be negetive
             
        if not u.flags & user.F_CHARGE:
            return False
        
        if u.msg_num - num < 0 and num > 0:
            return 0, {'rtype':'addmessage', 'num':num, 'errno':-2} #not enough message
        
        if not self.users.get(username):
            return False
        
        pu = self.users.get(username)
        if pu.uid == u.uid:
            return 0, {'rtype':'addmessage', 'num':num, 'errno':-3} #cannot be negetive
        
        if pu.parent_id != u.uid and not u.is_admin():
            return 0, {'rtype':'addmessage', 'num':num, 'errno':-4} #cannot be negetive
        
        if pu.msg_num + num >= 0:
            before_num = pu.msg_num
            pu.add_message(num)
            try:
                self.db.raw_sql('INSERT INTO addmsglog(username,before_msg_num,add_msg_num,after_msg_num,type,create_time) VALUES(%s,%s,%s,%s,%s,%s)',
                                (pu.username, before_num, num, pu.msg_num, 0, datetime.now()))
                logger.debug("processor_addmessage | username:%s | before_msg_num:%d | add_msg_num:%d | after_msg_num:%d | type:0"  
                                 % (pu.username, before_num, num, pu.msg_num))
            except:
                pass
            u.add_message(-num)
            return 0, {'rtype':'addmessage', 'num':num, 'errno': 0}
        else:
            return 0, {'rtype':'addmessage', 'num':num, 'errno':-1} #cannot be negetive
       
    def check_message_content(self, msg):
        pattern1 = re.compile('.*【.*】$')
        pattern2 = re.compile('^.*【.*】.*')
        if pattern1.match(msg) == None and pattern2.match(msg) == None:
            return False
        else:
            return True

    def check_addr(self, addr_list):
        pm = phonenumber.phonenumber()
        if len(addr_list) == 0:
            return False

    def __split_message(self, uid, addr_list, msg, status, channel, seed):
        msg_status = message.F_FAIL
        if self.check_message_content(msg):
            msg_status = message.F_ADMIT
        if channel == '106k':
            msg_status = message.F_ADMIT

        if channel in ('changshang_a_01', 'changshang_a_02',
                        'honglian_01',
                        'honglian_bjyh', 'honglian_jtyh',
                        '106g', '106ha', '106hb',
                        'honglian_ty', 'honglian_tyb', 'honglian_tyd', '106f_95559', '106f_95526'):
            addr = []
            for i in xrange(0, len(addr_list), 20):
                addr.append(addr_list[i: min(i + 20, len(addr_list))])
            for item in addr:
                new_message = message()        
                new_message.new(uid, ';'.join(item), 0, msg, msg_status, channel, len(addr_list), seed)
                self.messages[new_message.uid] = new_message
        elif channel in ('106j',):
            addr = []
            for i in xrange(0, len(addr_list), 5000):
                addr.append(addr_list[i: min(i + 5000, len(addr_list))])
            for item in addr:
                new_message = message()
                new_message.new(uid, ';'.join(item), 0, msg, msg_status, channel, len(addr_list), seed)
                self.messages[new_message.uid] = new_message
        elif channel in ('qixintong2012_01', 'qixintong2012_02', 'changshang_a_03'):
            addr = []
            for i in xrange(0, len(addr_list), 100):
                addr.append(addr_list[i: min(i + 100, len(addr_list))])
            for item in addr:
                new_message = message()
                new_message.new(uid, ';'.join(item), 0, msg, msg_status, channel, len(addr_list), seed)
                self.messages[new_message.uid] = new_message
        elif channel in ('hb_ct_01', 'hb_ct_02', 'hb_ct_03', 'hb_ct_04', 'hb_ct_05', 'maoming_ct_01'):
            addr = []
            for i in xrange(0, len(addr_list), 20):
                addr.append(addr_list[i: min(i + 20, len(addr_list))])
            for item in addr:
                new_message = message()        
                new_message.new(uid, ';'.join(item), 0, msg, msg_status, channel, len(addr_list), seed)
                self.messages[new_message.uid] = new_message  
        elif channel in ('shangxintong_01', ):
            addr = []
            for i in xrange(0, len(addr_list), 1):
                addr.append(addr_list[i: min(i + 1, len(addr_list))])
            for item in addr:
                new_message = message()        
                new_message.new(uid, ';'.join(item), 0, msg, msg_status, channel, len(addr_list), seed)
                self.messages[new_message.uid] = new_message     
        else:
            addr = []
            for i in xrange(0, len(addr_list), 20):
                addr.append(addr_list[i: min(i + 20, len(addr_list))])
            for item in addr:
                new_message = message()        
                new_message.new(uid, ';'.join(item), 0, msg, msg_status, channel, len(addr_list), seed)
                self.messages[new_message.uid] = new_message
     
    def processor_sendmessagelist(self, u, query): 
        #TODO
        lists = query['list']
        
        msg_postfix = u.msg_postfix.decode('utf8')
        itemindex = 0
        totalnum = 0
        for item in lists:
            try:
                print itemindex
                itemindex = itemindex + 1
                address = item[0]
                msg = item[1]
                
                logger.debug("processor_sendmessagelist | msg:%s | address_len:%d" % (msg, len(address)))
                
                p = 0
                msgcontent = ""
                try:
                    msgcontent = msg.decode('utf8')
                except:
                    try:
                        msg = msg.decode('gbk').encode('utf8')
                        msgcontent = msg.decode('utf8')
                    except:
                        return 0, {'rtype':'sendmessagelist', 'errno':-1} #unknow encoding
                
                p = 0
                if len(msgcontent) == 0:
                    p = 0
                elif len(msgcontent) + len(msg_postfix) <= 70:
                    p = 1
                elif len(msgcontent) <= 500:
                     p = (len(msgcontent) - 1) / (64 - len(msg_postfix)) + 1
                else:
                    return 0, {'rtype':'sendmessagelist', 'errno':-4} #zero message
                 
                num = p
                
                if num == 0:
                    return 0, {'rtype':'sendmessagelist', 'errno':-3} #zero message
                
                if u.msg_num < num:
                    return 0, {'rtype':'sendmessagelist', 'errno':-2} #not enough money 
                
                pm = phonenumber.phonenumber()
                split_addr = pm.split_addr([address])
                seed(time.time())
                my_seed = randint(0, 10000)
                for channel, addr in [(u.channel_cm, pm.S_CM)
                                       ,(u.channel_cu, pm.S_CU)
                                       ,(u.channel_ct, pm.S_CT)
                                       ]:
                    if p == 1 or channel in ['shangxintong_01', 'honglian_01',
                                             'honglian_bjyh',
                                             'honglian_jtyh',
                                             'honglian_ty',
                                             'honglian_tyb',
                                             'honglian_tyd',
                                             'changshang_a_01',
                                             'changshang_a_02',
                                             'changshang_a_04',
                                             'qixintong2012_01',
                                             'qixintong2012_02',
                                             'zhangshangtong_01',
                                             'zhangshangtong_02',
                                             'zhangshangtong_03',
                                             '106f_95559',
                                             '106f_95526',
                                             '106g',
                                             '106ha',
                                             '106hb',
                                             '106j',
                                             '106i',
                                             'cmpp_beijing_1',
                                             'hlyd_01',
                                             'changshang_a_03']:
                        if len(split_addr[addr]) > 0:
                            self.__split_message(u.uid, split_addr[addr], msg + msg_postfix.encode('utf8'), message.F_ADMIT, channel, my_seed)
                    else:
                        for i in range(p):
                            if len(split_addr[addr]) > 0:
                                self.__split_message(u.uid, split_addr[addr], "(" + str(i + 1) + "/" + str(p) + ")" + 
                                            msgcontent[i * (64 - len(msg_postfix)):(i + 1) * (64 - len(msg_postfix))].encode('utf8') + msg_postfix.encode('utf8'), message.F_ADMIT, channel, my_seed)
                totalnum += num
            except:
                pass
        return 0, {'rtype':'sendmessagelist', 'num':totalnum, 'errno': 0}
            
        pass          
    def processor_sendmessage(self, u, query):
        #{'q':'sendmessage, 'sid':sid, 'address':list of address, 'address_list' 'msg':message}
        #TODO
        if u.msg_num <= 0:
            return 0, {'rtype':'sendmessage', 'errno':-2} #not enough money 
  
        uid = u.uid
        address = query['address']
        address_list = query.get('address_list', 0)
        msg = query['msg']
        
        phone_type = query.get('type' , self.PHONE_NUMBER)
        logger.debug("processor_sendmessage | userid:%d | address_len:%d | type:%d" % (uid, len(address), phone_type))
        
        try:
            msgcontent = msg.decode('utf8')
        except:
            try:
                msg = msg.decode('gbk').encode('utf8')
                msgcontent = msg.decode('utf8')
            except:
                return 0, {'rtype':'sendmessage', 'errno':-1} #unknow encoding
            
        if len(address) == 0 and address_list == 0:
            return 0, {'rtype':'sendmessage', 'errno':-3} #zero message
        if len(msg) == 0:
            return 0, {'rtype':'sendmessage', 'errno':-3} #zero message
        
        
        #phone_name: load from addresslist table or load from address fields
        if phone_type == self.PHONE_NAME :
            numbers = []
            names = address.split(";")
            for name in names:
                print name
                addresslistobj = addresslist()
                addresslistobj.loadByName(uid, name)
                numbers.append(addresslistobj.number)
            number = ";".join(numbers)
            l = number.split(";")
        elif phone_type == self.PHONE_NUMBER:
            l = address.split(";")
        else:
            return 0, {'rtype':'sendmessage', 'errno':-6} #error type
        
        
        if l[len(l) - 1] == '':
            l.pop()
        if len(l) > 10000: #phone number less than 1000
            return 0, {'rtype':'sendmessage', 'errno':-5} #zero message
        
        msg_postfix = u.msg_postfix.decode('utf8')
        print len(msgcontent)

        p = 0
        if len(msgcontent) == 0:
            p = 0
        elif len(msgcontent) + len(msg_postfix) <= 70:
            p = 1
        elif len(msgcontent) <= 500:
            p = (len(msgcontent) - 1) / (64 - len(msg_postfix)) + 1
        else:
            return 0, {'rtype':'sendmessage', 'errno':-4} #zero message
         
        num = len(l) * p
        
        if num == 0:
            return 0, {'rtype':'sendmessage', 'errno':-3} #zero message
        
        if u.msg_num < num:
            return 0, {'rtype':'sendmessage', 'errno':-2} #not enough money 
        
        pm = phonenumber.phonenumber()
        split_addr = pm.split_addr(l)
        seed(time.time())
        my_seed = randint(0, 10000)
        for channel, addr in [(u.channel_cm, pm.S_CM)
                               ,(u.channel_cu, pm.S_CU)
                               ,(u.channel_ct, pm.S_CT)
                               ]:
            if p == 1 or channel in ['shangxintong_01', 'honglian_01',
                                     'honglian_bjyh',
                                     'honglian_jtyh',
                                     'honglian_ty',
                                     'honglian_tyb',
                                     'honglian_tyd',
                                     'changshang_a_01',
                                     'changshang_a_02',
                                     'changshang_a_04',
                                     'qixintong2012_01',
                                     'qixintong2012_02',
                                     'zhangshangtong_01',
                                     'zhangshangtong_02',
                                     'zhangshangtong_03',
                                     '106f_95559',
                                     '106f_95526',
                                     '106g',
                                     '106ha',
                                     '106hb',
                                     '106j',
                                     '106i',
                                     'cmpp_beijing_1',
                                     'hlyd_01',
                                     'changshang_a_03']:
                if len(split_addr[addr]) > 0:
                    self.__split_message(u.uid, split_addr[addr], msg + msg_postfix.encode('utf8'), message.F_ADMIT, channel, my_seed)
            else:
                for i in range(p):
                    if len(split_addr[addr]) > 0:
                        self.__split_message(u.uid, split_addr[addr], "(" + str(i + 1) + "/" + str(p) + ")" + 
                                    msgcontent[i * (64 - len(msg_postfix)):(i + 1) * (64 - len(msg_postfix))].encode('utf8') + msg_postfix.encode('utf8'), message.F_ADMIT, channel, my_seed)
                        
        return 0, {'rtype':'sendmessage', 'num':num, 'errno': 0}
    
    def processor_userinfo(self, user, query):
        #{'q':'userinfo', 'sid': sid}
        #TODO
        logger.debug("processor_userinfo | userinfo:%s" % user.to_json())
        return 0, {'rtype':'userinfo', 'user':user.to_json(), 'errno': 0}
    
    def processor_listchildren(self, u, query):
        #{'q':'listchildren', 'sid':sid}
        #TODO
        uid = u.uid
        u = self.user_ids[uid]
        l = []
        if u.is_admin() and u.username == 'root':
            for  value in self.user_ids.itervalues():
                if value.parent_id == 0:
                    l.append(value.to_json_all())
        else:
            l.append( u.to_json_all())
        logger.debug("processor_listchildren | children:%s" % l)
        return 0, {'rtype':'listchildren', 'children': l, 'errno': 0}

    def is_parent(self, id1, id2):
        if id2 not in self.user_ids:
            return False
        
        pid_dict = {}
        parent_id = self.user_ids[id2].parent_id
        pid_dict[parent_id] = 0
        while parent_id != 0:
            if id1 == parent_id:
                return True
            
            parent = self.user_ids[parent_id]
            if parent.parent_id in pid_dict:
                break
            
            parent_id = parent.parent_id
            pid_dict[parent_id] = 0
                        
        return False

    def processor_listmsg(self, u, query):
        #{'q':'listmsg', 'sid':sid, 'status':status}
        #TODO
        
        status = query['status']
        begin = query['begin'] / 1000.0
        end = query['end'] / 1000.0
        
        pbegin = datetime.fromtimestamp(begin)
        pend = datetime.fromtimestamp(end) + timedelta(1)
        where = 'create_time between %s and %s' % (pbegin.strftime('%Y%m%d'), pend.strftime('%Y%m%d'))
        self.reload_message(where)
        l = []
        for k in self.messages.itervalues():
            if k.user_uid == u.uid or u.flags & user.F_CREATE_CHARGE:
                if (status == 0 and k.status != message.F_DELETE) or k.status == status:
                    if ((k.last_update == None and (k.create_time >= pbegin and k.create_time <= pend))
                        or (k.last_update >= pbegin and k.last_update <= pend)):
                        if (u.username == "root") or self.is_parent(u.uid, k.user_uid) or u.uid == k.user_uid: 
                            try:
                                msg_json = k.to_json()
                                if(self.user_ids.get(k.user_uid)):
                                    msg_json['username'] = self.user_ids[k.user_uid].username
                                l.append(msg_json)
                            except:
                                pass
        
        logger.debug("processor_listmsg | status:%d | begin:%d | end:%d | msg_cnt:%d" % (status, begin, end, len(l)))
        
        return 0, {'rtype':'listmsg', 'msg':l, 'errno': 0}
    
    def processor_listcheckmsg(self, u, query):
        #{'q':'listcheckmsg', 'sid':sid, 'status':status}
        #TODO
        self.reload_message()
        if not u.is_admin():
            return False
        
        l = []
        for k in self.messages.itervalues():
            if k.status == message.F_COMMIT or k.status == message.F_REJECT:
                msg_json = k.to_json()
                if(self.user_ids.get(k.user_uid)):
                    msg_json['username'] = self.user_ids[k.user_uid].username
                l.append(msg_json)
        
        logger.debug("processor_listcheckmsg | list_checkmsg_cnt:%d" % len(l))
        return 0, {'rtype':'listcheckmsg', 'msg':l, 'errno': 0}
    
    def processor_msginfo(self, user, query):
        #{'q':'msginfo', 'sid':sid, 'id':msg_id}
        #TODO
        
        #cost too much
        self.reload_message()
        if 'id' not in query:
            return False
        
        msg_id = query['id']
        
        if not self.messages.get(msg_id):
            return False
        
        m = self.messages[msg_id]
        if m.uid != user.id:
            return False
        
        logger.debug("processor_msginfo | msg:%s" % m)
        return 0, {'rtype':'msginfo', 'msg':m, 'errno': 0} 
    
    def processor_setuserstatus(self, u, query):
        #{'q':'setuserstatus', 'sid':sid, user:username 'status':0 for disable, 1 for enable}
        #TODO
        status = query['status']
        username = query['user']
        
        if status != 0 and status != 1:
            return False
        
        if u.username == username:
            return False
        
        pu = self.users[username]
        
        if(pu.uid == u.uid):
            return {'rtype':'setuserstatus', 'errno': 1} 
        if u.is_admin():
            pu.set_status(status)
        else:
            if pu.parent_id != u.uid:
                return False
            pu.set_status(status)    
        
        return 0, {'rtype':'setuserstatus', 'errno': 0} 
    
    def processor_manageuser(self, u, query):
        #{'q':'manageuser, 'sid':sid, user:username, desc:description, pass:password, flags:flags
        # 'can_weblogin':can_weblogin, 'can_post':'can_post', 'need_check':need_check
        # 'cm':cm, 'cu':cu, 'ct':ct}
        #TODO
        pu = self.users[query['user']]
        desc = query['desc']
        flags = query['flags']
        can_weblogin = query['can_weblogin']
        can_post = query['can_post']
        need_check = query['need_check']
        cm = query['cm']
        cu = query['cu']
        ct = query['ct']
        ext = query['ext']
        percent = int(query['percent'])
        if(not u.is_admin() and not (u.is_agent()
          and pu.parent_id == u.uid)):
            return 0, {'rtype':'manageuser', 'errno': 1}
        
        d = None
        if (ext != None and ext != ''):
            logger.debug("processor_manageuser | username:%s | ext:%s" % (query['user'],ext))
            d = self.db.raw_sql_query('SELECT uid FROM user WHERE ext = %s' % (ext))

        if u.is_admin():
            logger.debug("processor_manageuser | username:%s | percent:%d" % (query['user'],percent))
            pu.percent = percent
            try:
                if d != None and len(d) >= 1:
                    if pu.uid != d[0] and pu.uid != u.uid:
                        return 0, {'rtype':'manageuser', 'errno':-3}
                if len(ext) > 0 and not ext.isdigit():
                    return 0, {'rtype':'manageuser', 'errno':-2} #ext is not number
        
                newext = ext
                if len(ext) > 50:
                    newext = ext[0:50]
                pu.set_ext(newext)
            except:
                if ext == None or ext == '':
                    pu.set_ext('')
                else:
                    return 0, {'rtype':'manageuser', 'errno':-2} #ext is not number
        if query.get('pass'):
            logger.debug("processor_manageuser | username:%s | change password:%s" % (query['user'],query['pass']))
            pu.change_password(query['pass'])
            
        logger.debug("processor_manageuser | username:%s | desc:%s | flags:%d | can_weblogin:%d | can_post:%d | need_check:%d" 
                     % (query['user'],desc, flags, can_weblogin, can_post, need_check))
        pu.change_info(desc, flags, can_weblogin, can_post, need_check)

        if not pu.is_admin():
            pu.change_cm_r(cm)
            pu.change_cu_r(cu)
            pu.change_ct_r(ct)
        else:
            pu.change_cm(cm)
            pu.change_cu(cu)
            pu.change_ct(ct)

        pu.save()
        return 0, {'rtype':'manageuser', 'errno': 0} 
    
    def processor_deleteuserlist(self, u, query):
        #TODO
        userlist = query['userlist']
        logger.debug("processor_deleteuserlist | userlist_tobedel:%s" % str(userlist))
        for ui in userlist:
            pu = self.users[ui]
            
            if(not u.is_admin() and not u.uid == pu.parent_id):
                return False
            
            if(len(pu.children) > 0):
                return 0, {'rtype':'deleteuserlist', 'errno':-1} #has children
            
            u.delete_child(pu)
            del self.users[pu.username]
            del self.user_ids[pu.uid]
            
        return 0, {'rtype':'deleteuserlist', 'errno': 0}

    def processor_deleteuser(self, u, query):
        #TODO
        username = query['user']
        logger.debug("processor_deleteuser | user_tobedel:%s" % username)
        pu = self.users[username]
        
        if(not u.is_admin()) and (not u.uid == pu.parent_id):
            return False
        
        if(len(pu.children) > 0):
            return 0, {'rtype':'deleteuser', 'errno':-1} #has children
        
        if u.uid == pu.parent_id:
            u.delete_child(pu)
        else:
            pureally = self.user_ids[pu.parent_id]
            pureally.delete_child(pu)
        del self.users[pu.username]
        return 0, {'rtype':'deleteuser', 'errno': 0}
            
    def change_msg_status(self, msg, status):
        msg.change_status(status)
        
    def processor_managemsg(self, u, query):
        #{'q':'managemsg', 'sid':sid, 'mlist':msg id array, 'status':status}
        #TODO
        self.reload_message()
        mlist = query['mlist']
        status = query['status']
        logger.debug("processor_managemsg | username:%s | msg_list:%s | change_status:%d" % (u.username, str(mlist), status))
        
        for mid in mlist:
            m = self.messages[mid]
            
            if u.is_admin():
                if status == message.F_REJECT:
                    if m.status == message.F_COMMIT or m.status == message.F_REJECT:
                        if m.status == message.F_COMMIT and self.user_ids.get(m.user_uid):
                            self.user_ids[m.user_uid].commit_num -= m.msg_num
                            #self.user_ids[m.user_uid].add_message(m.msg_num)
                        self.change_msg_status(m, message.F_REJECT)
                    else:
                        return False
                elif status == message.F_ADMIT:
                    if m.status == message.F_COMMIT or m.status == message.F_REJECT:
                        if m.status == message.F_COMMIT and self.user_ids.get(m.user_uid):
                            self.user_ids[m.user_uid].commit_num -= m.msg_num
                        if m.status != message.F_COMMIT:
                            #self.user_ids[m.user_uid].add_message(-m.msg_num)
                            pass
                        self.change_msg_status(m, message.F_ADMIT)

                    else:
                        return False
                elif status == message.F_DELETE:                
                    if self.user_ids.get(m.user_uid):
                        if (m.status == message.F_COMMIT or m.status == message.F_ADMIT) :
                            #self.user_ids[m.user_uid].add_message(m.msg_num)
                            pass
                        if m.status == message.F_COMMIT:
                            self.user_ids[m.user_uid].commit_num -= m.msg_num
                    self.change_msg_status(m, message.F_DELETE)
                else:
                    return False
            elif u.username == m.username:
                if status == message.F_CANCEL:
                    if m.status == message.F_COMMIT:
                        #u.add_message(m.msg_num)
                        u.commit_num -= m.msg_num
                        self.change_msg_status(m, message.F_CANCEL)
                    else:
                        return False
                elif m.status == message.F_DELETE:
                        if (m.status == message.F_COMMIT or m.status == message.F_ADMIT) :
                            #u.add_message(m.msg_num)
                            pass
                        if m.status == message.F_COMMIT:
                            u.commit_num -= m.msg_num
                        self.change_msg_status(m, message.F_DELETE)
            else:
                return False

        return 0, {'rtype':'managemsg', 'errno': 0} 
            
    def processor_queryreport(self, u, query):
        #{q:'queryreport',sid:this.session, user:username, degin:start.time, end:end.time, type:type}
        #TODO 

        if('begin' not in query or 'end' not in query or
            'user' not in query):
            return False

        
        username = query['user']
        begin = query['begin'] / 1000.0
        end = query['end'] / 1000.0
        pbegin = datetime.fromtimestamp(begin)
        pend = datetime.fromtimestamp(end) + timedelta(1)
        where = 'create_time between %s and %s' % (pbegin.strftime('%Y%m%d'), pend.strftime('%Y%m%d'))
        self.reload_message(where)
        pm = phonenumber.phonenumber()
        logger.debug("processor_queryreport | begin:%s | end:%s | query_msg_cnt:%d " 
                     % (pbegin.strftime('%Y%m%d'), pend.strftime('%Y%m%d'), len(self.messages)))
        #send_user:send_num:success_num:fail_num:append_num
        l = []
        if username != None and username != "" and self.users.has_key(username):
            if not ((u.username == "root") or self.is_parent(u.uid, self.users[username].user_uid)):
                pass 
            keys = username
            u = self.users[keys]
            msg_json = {'send_user':keys, 'send_num':0, 'success_num':0, 'fail_num':0, 'append_num':0,
                                'cm_d_num':0, 'ct_d_num':0, 'cu_d_num':0,
                                'cm_s_num':0, 'ct_s_num':0, 'cu_s_num':0,
                                'cm_f_num':0, 'ct_f_num':0, 'cu_f_num':0,
                                'cm_a_num':0, 'ct_a_num':0, 'cu_a_num':0, 'sum_num':0}
            for k in self.messages.itervalues(): 
                    
                if k.user_uid == u.uid and pbegin <= k.create_time and k.create_time <= pend:
                    addr = k.address.split(';')
                    split_addr = pm.split_addr(addr)
                    msg_r = 0
                    if len(addr) > 0:
                        msg_r = k.msg_num / len(addr)
                    msg_json['send_user'] = username;                    
                    msg_json['send_num'] = msg_json['send_num'] + k.msg_num;
                    msg_json['cm_d_num'] = msg_json['cm_d_num'] + len(split_addr[pm.S_CM]) * msg_r
                    msg_json['ct_d_num'] = msg_json['ct_d_num'] + len(split_addr[pm.S_CT]) * msg_r
                    msg_json['cu_d_num'] = msg_json['cu_d_num'] + len(split_addr[pm.S_CU]) * msg_r
                    if k.status == k.F_SEND:
                        msg_json['success_num'] = msg_json['success_num'] + k.msg_num
                        msg_json['cm_s_num'] = msg_json['cm_s_num'] + len(split_addr[pm.S_CM]) * msg_r
                        msg_json['ct_s_num'] = msg_json['ct_s_num'] + len(split_addr[pm.S_CT]) * msg_r
                        msg_json['cu_s_num'] = msg_json['cu_s_num'] + len(split_addr[pm.S_CU]) * msg_r
                    elif k.status == k.F_FAIL:  
                        msg_json['fail_num'] = msg_json['fail_num'] + k.msg_num   
                        msg_json['cm_f_num'] = msg_json['cm_f_num'] + len(split_addr[pm.S_CM]) * msg_r
                        msg_json['ct_f_num'] = msg_json['ct_f_num'] + len(split_addr[pm.S_CT]) * msg_r
                        msg_json['cu_f_num'] = msg_json['cu_f_num'] + len(split_addr[pm.S_CU]) * msg_r 
                    elif k.status == k.F_ADMIT:
                        msg_json['append_num'] = msg_json['append_num'] + k.msg_num
                        msg_json['cm_a_num'] = msg_json['cm_a_num'] + len(split_addr[pm.S_CM]) * msg_r
                        msg_json['ct_a_num'] = msg_json['ct_a_num'] + len(split_addr[pm.S_CT]) * msg_r
                        msg_json['cu_a_num'] = msg_json['cu_a_num'] + len(split_addr[pm.S_CU]) * msg_r
                            
            l.append(msg_json)   
        else:
            messages = {}
            for k in self.messages.itervalues():
                if k.user_uid not in messages:
                    tmp = []
                else:
                    tmp = messages[k.user_uid]
                tmp.append(k)
                messages[k.user_uid] = tmp
            
            pid = u.uid
            msg_json = self.get_message(messages, pid, pbegin, pend)
            l.append(msg_json)
        return 0, {'rtype':'queryreport', 'msg':l, 'errno': 0} 
    
    def get_message(self, message, pid, pbegin, pend):
        #TODO
        pu = self.user_ids[pid]
        keys = pu.username
        msg_json = {'send_user':keys, 'send_num':0, 'success_num':0, 'fail_num':0, 'append_num':0,
                    'cm_d_num':0, 'ct_d_num':0, 'cu_d_num':0,
                    'cm_s_num':0, 'ct_s_num':0, 'cu_s_num':0,
                    'cm_f_num':0, 'ct_f_num':0, 'cu_f_num':0,
                    'cm_a_num':0, 'ct_a_num':0, 'cu_a_num':0}        
        if pid in message:
            pm = phonenumber.phonenumber()
            tmp = message[pid]
            for k in tmp:
                if k.user_uid == pu.uid and pbegin <= k.create_time and k.create_time <= pend:
                    addr = k.address.split(';')
                    split_addr = pm.split_addr(addr)
                    msg_r = 0
                    if len(addr) > 0:
                        msg_r = k.msg_num / len(addr)
                    #msg_json['send_user'] = username;                    
                    msg_json['send_num'] = msg_json['send_num'] + k.msg_num;
                    msg_json['cm_d_num'] = msg_json['cm_d_num'] + len(split_addr[pm.S_CM]) * msg_r
                    msg_json['ct_d_num'] = msg_json['ct_d_num'] + len(split_addr[pm.S_CT]) * msg_r
                    msg_json['cu_d_num'] = msg_json['cu_d_num'] + len(split_addr[pm.S_CU]) * msg_r
                    if k.status == k.F_SEND:
                        msg_json['success_num'] = msg_json['success_num'] + k.msg_num
                        msg_json['cm_s_num'] = msg_json['cm_s_num'] + len(split_addr[pm.S_CM]) * msg_r
                        msg_json['ct_s_num'] = msg_json['ct_s_num'] + len(split_addr[pm.S_CT]) * msg_r
                        msg_json['cu_s_num'] = msg_json['cu_s_num'] + len(split_addr[pm.S_CU]) * msg_r
                    elif k.status == k.F_FAIL:  
                        msg_json['fail_num'] = msg_json['fail_num'] + k.msg_num
                        msg_json['cm_f_num'] = msg_json['cm_f_num'] + len(split_addr[pm.S_CM]) * msg_r
                        msg_json['ct_f_num'] = msg_json['ct_f_num'] + len(split_addr[pm.S_CT]) * msg_r
                        msg_json['cu_f_num'] = msg_json['cu_f_num'] + len(split_addr[pm.S_CU]) * msg_r      
                    elif k.status == k.F_ADMIT:
                        msg_json['append_num'] = msg_json['append_num'] + k.msg_num
                        msg_json['cm_a_num'] = msg_json['cm_a_num'] + len(split_addr[pm.S_CM]) * msg_r
                        msg_json['ct_a_num'] = msg_json['ct_a_num'] + len(split_addr[pm.S_CT]) * msg_r
                        msg_json['cu_a_num'] = msg_json['cu_a_num'] + len(split_addr[pm.S_CU]) * msg_r
        l = []
        for i in pu.children.itervalues():
            msg_json_children = self.get_message(message, i.uid, pbegin, pend)
            l.append(msg_json_children)
        msg_json['children'] = l
        return msg_json
    
    def special_channel_upload(self, u, begin, end, l):
        #TODO
        channels = [u.channel_cm, u.channel_cu, u.channel_ct]
        ext_numbers = special_channel(channels)
        for ext in ext_numbers:
            d = self.db.raw_sql_query('SELECT ext, number, content, time FROM upload_msg WHERE ext = "%s" and time >= "%s" and time <= "%s"' % (ext, begin, end))
            if d != None:
                for ext, number, content, time in d:
                    try:
                        content.decode('utf8')
                    except:
                        try:
                            content = content.decode('gbk').encode('utf8')
                        except:
                            pass
                    i = {'ext':ext, 'number':number, 'content':content, 'username':u.description, 'time':time.isoformat(' '), 'userid':u.username}
                    l.append(i)    
        return l
    
    def processor_uploadreport(self, u, query):
        #TODO
        if('begin' not in query or 'end' not in query or
            'user' not in query):
            return False
        
        username = query['user']
        begin = query['begin'] / 1000.0
        end = query['end'] / 1000.0
        pbegin = datetime.fromtimestamp(begin)
        pend = datetime.fromtimestamp(end) + timedelta(1)
        
        l = []
        if not u.is_admin():
            username = u.username
            keys = username
            u = self.users[keys]
            
            
            d = self.db.raw_sql_query('SELECT ext, number, content, time FROM upload_msg WHERE ext = "%s" and time >= "%s" and time <= "%s"' % (u.ext, pbegin, pend))
            if d != None and u.ext != None and u.ext != '':
                for ext, number, content, time in d:
                    try:
                        content.decode('utf8')
                    except:
                        try:
                            content = content.decode('gbk').encode('utf8')
                        except:
                            pass
                    i = {'ext':ext, 'number':number, 'content':content, 'username':u.description, 'time':time.isoformat(' '), 'userid':username}
                    l.append(i)    
            self.special_channel_upload(u, pbegin, pend, l)
        elif (username != None and username != "" and self.users.has_key(username)):
            keys = username
            if self.is_parent(u.uid, self.users[keys].uid) :
                u = self.users[keys]                
                
                d = self.db.raw_sql_query('SELECT ext, number, content, time FROM upload_msg WHERE ext = "%s" and time >= "%s" and time <= "%s"' % (u.ext, pbegin, pend))
                if d != None and u.ext != None and u.ext != '':
                    for ext, number, content, time in d:
                        try:
                            content.decode('utf8')
                        except:
                            try:
                                content = content.decode('gbk').encode('utf8')
                            except:
                                pass
                        i = {'ext':ext, 'number':number, 'content':content, 'username':u.description, 'time':time.isoformat(' '), 'userid':username}
                        l.append(i)
                self.special_channel_upload(u, pbegin, pend, l)
        else:
            for keys in self.user_ids.keys():
                if (u.username == "root") or (u.uid == keys) or(self.is_parent(u.uid, keys)):
                    pu = self.user_ids[keys]  
                    self.special_channel_upload(pu, pbegin, pend, l)
                    if pu.ext == None or pu.ext == '':
                        continue
                    d = self.db.raw_sql_query('SELECT ext, number, content, time FROM upload_msg WHERE ext = "%s" and time >= "%s" and time <= "%s"' % (pu.ext, pbegin, pend))
                    if d == None or len(d) == 0:
                        continue
                    for ext, number, content, time in d:
                        try:
                            content.decode('utf8')
                        except:
                            try:
                                content = content.decode('gbk').encode('utf8')
                            except:
                                pass
                        i = {'ext':ext, 'number':number, 'content':content, 'username':u.description, 'time':time.isoformat(' '), 'userid':u.username}
                        l.append(i)
                    
        
        return 0, {'rtype':'uploadreport', 'msg':l, 'errno': 0}     

    def processor_channelqueryreport(self, u, query):
        #{q:'queryreport',sid:this.session, degin:start.time, end:end.time, type:type}
        #TODO 

        if('begin' not in query or 'end' not in query):
            return False
       
        begin = query['begin'] / 1000.0
        end = query['end'] / 1000.0
        pbegin = datetime.fromtimestamp(begin)
        pend = datetime.fromtimestamp(end) + timedelta(1)
        where = 'create_time between %s and %s' % (pbegin.strftime('%Y%m%d'), pend.strftime('%Y%m%d'))
        sql = '''select channel, status, sum(msg_num), sum(sub_num)  from message where %s  group by channel, status;
        ''' % where
        q = self.db.raw_sql_query(sql)
 
        msg_dict = {}
        total = {'send_num':0, 'success_num':0, 'fail_num':0, 'append_num':0, 'sub_num':0}
        for channel, status, msg_num, sub_num in q:
            if channel == 'default':
                channel = 'hb_ct_01'
            if channel not in msg_dict.keys():
                msg_json = {'send_num':0, 'success_num':0, 'fail_num':0, 'append_num':0, 'sub_num':0}
            else:
                msg_json = msg_dict[channel]
            
            if status == message.F_SEND:
                msg_json['success_num'] += int(msg_num)
                msg_json['sub_num'] += int(sub_num)
            elif status == message.F_FAIL:
                msg_json['fail_num'] += int(msg_num)
            elif status == message.F_ADMIT:
                msg_json['append_num'] +=  int(msg_num)
            msg_json['send_num'] += int(msg_num)
            msg_dict[channel] = msg_json
            print msg_json
            
        for v in msg_dict.values():
            for key, value in v.iteritems():
                total[key] += value
        msg_dict['total'] = total
        result = []
        for channel, msg_json in msg_dict.items():
            msg_json['channel'] = channel
            result.append(msg_json)
                                        
        return 0, {'rtype':'channelqueryreport', 'result':result, 'errno': 0}     
    
    def processor_addmsglog(self, u, query):
        #{q:'queryreport',sid:this.session, user:username, degin:start.time, end:end.time, type:type}
        #TODO 
        if('begin' not in query or 'end' not in query):
            return False
        begin = query['begin'] / 1000.0
        end = query['end'] / 1000.0
        pbegin = datetime.fromtimestamp(begin)
        pend = datetime.fromtimestamp(end) + timedelta(1)

        q = self.db.raw_sql_query('SELECT uid, username, before_msg_num, add_msg_num, after_msg_num, type, create_time FROM addmsglog WHERE create_time >= %s and create_time <= %s', (pbegin, pend))
    
        l = []
        index = 0
        for uid, username, before_msg_num, add_msg_num, after_msg_num, msg_type, create_time in q:
            try:
                if(u.username == "root" or (self.users.get(username) and
                                    (self.is_parent(u.uid, self.users[username].uid) or
                                     self.users[username].uid == u.uid))):
                    type_text = "直接充值"
                    if msg_type == 1:
                        type_text = "返还"
                    index = index + 1
                    uid = uid
                    l.append({'uid':index,
                              'username':username,
                              'before_msg_num':before_msg_num,
                              'add_msg_num':add_msg_num,
                              'after_msg_num':after_msg_num,
                              'type':type_text,
                              'create_time':create_time.strftime("%y-%m-%d %H:%M")})
                
            except:
                pass
        return 0, {'rtype':'addmsglog', 'msg':l, 'errno': 0}     
        

    def processor_listlog(self, user, query):
        #TODO
        if('begin_year' not in query or 'begin_month' not in query or
            'begin_day' not in query or 'end_year' not in query or
             'end_month' not in query or 'end_day' not in query or
             'action' not in query):
            return False
        
        begin_year = query['begin_year']
        begin_month = query['begin_month']
        begin_day = query['begin_day']
        end_year = query['end_year']
        end_month = query['end_month']
        end_day = query['end_day']
        
        begin = datetime(begin_year, begin_month, begin_day)
        end = datetime(end_year, end_month, end_day + 1)
        
        if query['action'] == 'all':
            if not user.has_right('listlog_all'):
                return False                 
            l = []
            for i in self.logs:
                if i.datetime >= begin and i.datetime <= end:
                    l.append(i.to_json())
                
        elif query['action'] == 'children':
            if not user.has_right('listlog_children'):
                return False
            l = []
            for i in self.logs:
                if i.datetime >= begin and i.datetime <= end and user.is_parent(i.username):
                    l.append(i.to_json())
        elif query['action'] == 'self':
            l = []
            for i in self.logs:
                if i.datetime >= begin and i.datetime <= end and user.username == i.username:
                    l.append(i.to_json())
            pass
        
        else:
            return False
        
        return 0, {'rtype':'listlog', 'l':l}
    
    def processor_getphonebookinfo(self, user, query):
        #TODO
        uid = user.uid
        phonebook.set_db(self.db, 'phonebook')
        phonebooks = phonebook.load('user_uid = %s', uid)        
        l = []
        for item in phonebooks:
            l.append(item.to_json())
        return 0, {'rtype':'getphonebookinfo', 'list':l}
        
    def processor_addphonebook(self, user, query):
        #{'q':'addphonebook', 'sid': sid, 'name':name, 'remark':remark}  
        #TODO
        if ('name' not in query or 'remark' not in query):
            return False      
        
        uid = user.uid
        phonebook.set_db(self.db, 'phonebook')
        name = query['name']
        remark = query['remark']
                        
        new_phonebook = phonebook()
        new_phonebook.new(uid, name, remark)        
        return 0, {'rtype':'addphonebook', 'errno' : 0} #成功
    
    def processor_managephonebook(self, user, query):
        #{'q':'managephonebook', 'sid': sid, 'id':uid, 'name':name, 'remark':remark}  
        #TODO
        if ('id' not in query or 'name' not in query or 'remark' not in query):
            return False      
        
        uid = user.uid
        phonebook_id = query['id']
        phonebook.set_db(self.db, "phonebook")
        phonebook_old = phonebook()
        phonebook_old.loadByID(uid, phonebook_id)
        phonebook_old.name = query['name']
        phonebook_old.remark = query['remark']
        phonebook_old.save('name,remark')
        return 0, {'rtype':'managephonebook', 'errno' : 0} #成功        
    
    def processor_deletephonebook(self, user, query):
        #TODO
        if 'id' not in query:
            return False
        
        uid = user.uid
        phonebook_id = query['id']
        phonebook.set_db(self.db, 'phonebook')
        phonebook_old = phonebook()
        phone.set_db(self.db, 'phone')
        phone_old = phone()
        phone_old.deleteByPhonebookUid(phonebook_id)
        phonebook_old.loadByID(uid, phonebook_id)
        phonebook_old.delete()
    
        return 0, {'rtype':'deletephonebook', 'errno':0}
    
    def processor_getaddresslistinfo(self, user, query):
        #TODO
        uid = user.uid
        addresslist.set_db(self.db, 'address')
        addresslists = addresslist.load('user_uid = %s', uid)        
        l = []
        for item in addresslists:
            l.append(item.to_json())
        return 0, {'rtype':'getaddresslistinfo', 'list':l}
    
    def processor_addaddresslist(self, user, query):
        #TODO
        if ('addresslist' not in query or 'name' not in query):
            return False
        
        print 'begin get the info'
        uid = user.uid
        addresslist.set_db(self.db, 'address')
        address = query['addresslist']
        name = query['name']
        if len(address) == 0 :
            return 0, {'rtype':'addaddresslist', 'errno':-1} #zero address
        
        print 'begin to check addresslist'
        new_addresslist = addresslist()
        new_addresslist.new(uid, name, address)
        return 0, {'rtype':'addaddresslist', 'errno':0}
    
    def processor_deleteaddresslist(self, user, query):
        #TODO
        if 'addresslist' not in query:
            return False
        
        print 'begin to delete addresslist'
        uid = user.uid
        addresslist.set_db(self.db, 'address')
        address = query['addresslist']
        print len(address)
        print address
        if len(address) == 0:
            print 'delete adddresslist error.'
            return 0, {'rtype':'deleteaddresslist', 'errno':-1}  #zero address
        
        l = address.split(";")
        if l[len(l) - 1] == '':
            l.pop()
        print len(l)
        for name in l:
            print name
            new_addresslist = addresslist()
            new_addresslist.deleteOne(uid, name)
    
        return 0, {'rtype':'deleteaddresslist', 'errno':0}
    
    def processor_getphonelistdata(self, user, query):
        #TODO
        if 'id' not in query:
            return False
        
        phone.set_db(self.db, 'phone')
        phonebook_uid = query['id']
        phones = phone.load('phonebook_uid = %s', phonebook_uid)   
        l = []
        for item in phones:
            l.append(item.to_json())
        return 0, {'rtype':'getphonelistdata', 'list':l}
    
    def processor_getallphoneinfo(self, user, query):
        #TODO
        uid = user.uid
        phonebook.set_db(self.db, 'phonebook')
        phonebooks = phonebook.load('user_uid = %s', uid)        
        l = []
        phone.set_db(self.db, 'phone')
        for item in phonebooks:
            phonebook_uid = item.uid
            phones = phone.load('phonebook_uid = %s', phonebook_uid)   
            for obj in phones:
                l.append(obj.to_json())
        return 0, {'rtype':'getallphoneinfo', 'list':l}        
    
    def processor_addphone(self, user, query):
        #{'q':'addphone', 'sid': sid, 'phonebook_id':phonebook_id, 
        # 'name':name, 'companyname':companyname, 'title':title, 'mobile':mobile}  
        #TODO
        if ('phonebook_id' not in query or'name' not in query 
            or 'companyname' not in query or 'mobile' not in query 
            or 'title' not in query):
            return False      
        
        phone.set_db(self.db, 'phone')
        phonebook_uid = query['phonebook_id']
        name = query['name']
        companyname = query['companyname']
        mobile = query['mobile']
        title = query['title']
        
                        
        new_phone = phone()
        new_phone.new(phonebook_uid, name, companyname, title, mobile)        
        return 0, {'rtype':'addphone', 'errno' : 0} #成功
    
    def processor_managephone(self, user, query):
        #{'q':'addphone', 'sid': sid, 'id':phone_id, 'phonebook_id':phonebook_id, 
        # 'name':name, 'companyname':companyname, 'title':title, 'mobile':mobile} 
        #TODO
        if ('id' not in query or 'phonebook_id' not in query or'name' not in query 
            or 'companyname' not in query or 'mobile' not in query 
            or 'title' not in query):
            return False      
        
        phone_id = query['id']
        phonebook_id = query['phonebook_id']
        phone.set_db(self.db, "phone")
        phone_old = phone()
        phone_old.loadByID(phonebook_id, phone_id)
        phone_old.name = query['name']
        phone_old.companyname = query['companyname']
        phone_old.mobile = query['mobile']
        phone_old.title = query['title']
        phone_old.save('name,companyname,mobile,title')
        return 0, {'rtype':'managephone', 'errno' : 0} #成功        
    
    def processor_deletephonelist(self, user, query):
        #{'q':'deletephonelist', 'sid':sid, 'phonelist':phonelist}
        #TODO
        if ('phonelist' not in query):
            return False
        
        l = query['phonelist']
        for uid in l:
            phone.set_db(self.db, 'phone')
            phone_old = phone()
            phone_old.uid = uid
            phone_old.delete()
        return 0, {'rtype':'deletephonelist', 'errno':0} #成功
    
    def processor_addphonelist(self, user, query):
        #{'q':'addphonelist', 'sid':sid, 'phonebook_name':phonebook_name, 'phonelist':addrs}
        if ('phonebook_name' not in query or 'phonelist' not in query):
            return False
        #TODO
        uid = user.uid
        phonebook.set_db(self.db, 'phonebook')
        phonebook_name = query['phonebook_name']
        remark = ''
                        
        new_phonebook = phonebook()
        new_phonebook.new(uid, phonebook_name, remark)
        phonebook_uid = new_phonebook.uid
        
        phone.set_db(self.db, 'phone')
        phonelist = query['phonelist']
        for phoneInfo in phonelist:
            print phoneInfo
            name = phoneInfo['name']
            companyname = phoneInfo['companyname']
            title = phoneInfo['title']
            mobile = phoneInfo['mobile']
            new_phone = phone()
            new_phone.new(phonebook_uid, name, companyname, title, mobile)
        return 0, {'rtype':'addphonelist', 'errno':0} #成功 
    
    def processor_change_user_msg_postfix(self, u, query):
        if ('msg_postfix' not in query):
            return False
        pu = self.users[query['user']]
        if(not u.is_admin() and not (u.is_agent()
            and pu.parent_id == u.uid)):
            return 0, {'rtype':'change_user_msg_postfix', 'errno': 1}
        
        msg_postfix = query['msg_postfix']
        if ('all_children' in query) and query['all_children'] == True:
            ret = pu.set_all_child_msg_postfix(msg_postfix)
        else:
            ret = pu.set_msg_postfix(msg_postfix)
            
        return 0, {'rtype':'change_user_msg_postfix', 'errno':ret}
    
def wsgiref_daemon():
    port = 8082
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, smsd('smsd.ini', True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    wsgiref_daemon()
else:
    application = smsd(conf=smsd_path + '/smsd.ini')
