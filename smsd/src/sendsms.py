# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from traceback import print_exc
from hashlib import sha1
from datetime import datetime
import phonenumber
from random import *
from time import time
import sys
if __name__ != '__main__':
    smsd_path = '/home/jimmyz/smsd/src'
    #smsd_path = 'C:\\xampp\\htdocs\\smsd\\src'
    sys.path.append(smsd_path)

from utils import urldecode
from loadcfg import loadcfg
from dbsql import dbsql

from message import message

class sendsms(object):
    def __init__(self, conf = 'smsd.ini', using_wsgiref = False):
        if not using_wsgiref:
            print '%s instance created, id 0x%08x' % \
                (self.__class__.__name__, id(self))
        self.num_req = 0
        self.cfg = loadcfg(conf)
        self.db = dbsql(**self.cfg.database.raw_dict)
    
    def __del__(self):
        print '%s instance 0x%08x destroyed, %d request(s) processed' % \
            (self.__class__.__name__, id(self), self.num_req)
        
    def __call__(self, env, start_response):
        # request handler
        self.num_req += 1
        if env['REQUEST_METHOD'] != 'POST' or 'CONTENT_LENGTH' not in env:
            return self.__ret(env, start_response, -99, 'invalid query, not POST or invalid POST length')
        length = int(env['CONTENT_LENGTH'])
        if length <= 0:
            return self.__ret(env, start_response, -99, 'error, empty POST body')
        try:
            post_data = env['wsgi.input'].read(length)
        except:
            print 'error reading POST data'
            print_exc()
            return self.__ret(env, start_response, -99, 'unknown error')
        try:
            query = urldecode(post_data)
        except:
            print 'error parsing query: %s' % post_data
            print_exc()
            return self.__ret(env, start_response, -99, 'invalid query, error parsing')
        
        username = query.get('user')
        password = query.get('pass')
        recv = query.get('recv')
        msg = query.get('msg')
        passtype = query.get('passtype')
        try:
            msgdecode = msg.decode('utf8')
        except:
            try:
                msg = msg.decode('gbk').encode('utf8')
            except:
                return self.__ret(env, start_response, -99, 'unknown message encoding neither utf-8 nor gbk')
            
        if username == None or username == '':
            return self.__ret(env, start_response, -99, 'invalid query, no user')
        if password == None or password == '':
            return self.__ret(env, start_response, -99, 'invalid query, no pass')
        if recv == None or recv == '':
            return self.__ret(env, start_response, -99, 'invalid query, no recv')
        if msg == None or msg == '':
            return self.__ret(env, start_response, -99, 'invalid query, no msg')
        if passtype == None or passtype == '':
            passtype = 'normal'
        elif passtype == 'sha1':
            passtype = 'sha1'
        else:
            passtype = 'normal'
        user_uid, remain = self.__check_user(username, password, passtype)
        if user_uid == None:
            return self.__ret(env, start_response, -1, 'user not exist or wrong pass')
        elif remain < 1:
            return self.__ret(env, start_response, -2, 'not enough credit')
        else:
            if len(recv.split(';')) > 1000:
                return self.__ret(env, start_response, -3, 'not support more than 1000 address');
            for addr in recv.split(';'):
                if len(addr) != 11:
                    return self.__ret(env, start_response, -4, 'some address error, use \';\' to split address number');
            ret = self.__send(user_uid, recv, msg)
            return self.__ret(env, start_response, ret)

        
    def __ret(self, env, start_response, errno, message = None):
        start_response('200 OK', [('Content_type', 'text/plain')])
        if self.cfg.sendsms.verbose > 0 and message != None:
            return ['%d,%s' % (errno, message)]
        elif errno > 0:
            return ['%d,%d,message commit success' % (1, errno)]
        else :
            return ['%d' % (errno)]
    
    def __get_user_channel(self, u):
        ret = self.db.raw_sql_query('SELECT channel_cm FROM user WHERE uid = %s', (u))
        if(len(ret) == 0):
            return None
        return ret[0][0]
    def __check_user(self, u, p,type):
        password = p
        if type == 'normal':
            password = sha1(p).hexdigest()
            
        ret = self.db.raw_sql_query('SELECT uid,msg_num FROM user WHERE username = %s AND password = %s AND can_post = TRUE AND need_check = FALSE',
                                    (u, password))
        if len(ret) == 0:
            return None, None
        user_uid, msg_num = ret[0]
        pending = self.db.raw_sql_query('SELECT SUM(msg_num) FROM message WHERE user_uid = %s AND status = %s',
                                        (user_uid, message.F_ADMIT))[0][0]
        return user_uid, msg_num - (pending or 0)
    
    def __send(self, u, recv, msg):
        ret = 0
        try:
            recv_list = self.__split_message(recv.split(';'))
            for new_recv in recv_list:
                channel = self.__get_user_channel(u)
                msg_num = ((len(msg.decode('utf8').encode('gbk')) - 1) / 140 + 1) * len(new_recv)
                self.db.raw_sql('INSERT INTO message(user_uid,address,msg,msg_num,status,create_time,channel) VALUES(%s,%s,%s,%s,%s,%s,%s)',
                                (u, ';'.join(new_recv), msg, msg_num, message.F_ADMIT, datetime.now(), channel))

                ret += msg_num
        except:
            pass
        return ret
        
    def __split_message(self, recv):
        pm = phonenumber.phonenumber()
        split_addr = pm.split_addr(recv)
        recv_list = []
        l = [pm.S_CM, pm.S_CU, pm.S_CT]
        for item_index in l:
            item = split_addr[item_index]
            new_l =  [[item[i] for i in range(a, min(a+20, len(item)))] for a in range(0, len(item), 20)]
            for k in new_l:
                if k:
                    recv_list.append(k)
        
        return recv_list
        

def wsgiref_daemon():
    port = 8080
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, sendsms(using_wsgiref = True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    wsgiref_daemon()
else:
    application = sendsms(conf = smsd_path + '/smsd.ini')
