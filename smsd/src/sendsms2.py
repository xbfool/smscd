# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from traceback import print_exc
from hashlib import sha1
from datetime import datetime
import phonenumber
from random import *
from time import time
import sys
import os
if __name__ != '__main__':
    smsd_path = os.path.dirname(__file__)
    #smsd_path = 'C:\\xampp\\htdocs\\smsd\\src'
    sys.path.append(smsd_path)

from utils import urldecode
from loadcfg import loadcfg
from dbsql import dbsql

from message import message
import logging
import httplib, urllib
import logging.handlers
import json
smsd_url = 'fudaduanxin.com'
smsd_port = '81'
from traceback import print_exc
class sendsms2(object):
    def __init__(self, conf = 'smsd.ini', using_wsgiref = False):
        if not using_wsgiref:
            print '%s instance created, id 0x%08x' % \
                (self.__class__.__name__, id(self))
        self.num_req = 0
        self.cfg = loadcfg(conf)
        self.db = dbsql(**self.cfg.database.raw_dict)
        LOG_FILENAME = '/var/log/smscd/sendsms2.log'
               
        my_logger = logging.getLogger('smsd.sendsms2')
        my_logger.setLevel(logging.DEBUG)
        # Add the log message handler to the logger

        handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=10000000, backupCount=2)
        my_logger.addHandler(handler)
        
        handler.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # add formatter to ch
        handler.setFormatter(formatter)


        self.logger = my_logger
        

    def __del__(self):
        print '%s instance 0x%08x destroyed, %d request(s) processed' % \
            (self.__class__.__name__, id(self), self.num_req)

    def __call__(self, env, start_response):
        self.logger.debug('request: %s' % env)
        self.num_req += 1
        if env['REQUEST_METHOD'] != 'GET':
            return self.__ret(env, start_response, 99, 'Error: please send via GET method')

        data = env['QUERY_STRING']
        query = urldecode(data)

        username = query.get('username')
        password = query.get('password')
        phone = query.get('phone')
        message = query.get('message')
        if username is None:
            return self.__ret(env, start_response, 4, 'Error: username is empty')
        if password is None:
            return self.__ret(env, start_response, 5, 'Error: password is empty')
        if phone is None:
            return self.__ret(env, start_response, 2, 'Error: phone is empty')
        if message is None:
            return self.__ret(env, start_response, 3, 'Error: message is empty')

        user_pass_ret = self.check_user_pass(username, password)
        if user_pass_ret == -1:
            return self.__ret(env, start_response, 6, 'Error: username and password not match')
        elif user_pass_ret == -2:
            return self.__ret(env, start_response, 8, 'Error: your account have not enough money')


        try:
            auth_ret = self.auth(username, password)
            sid = auth_ret['sid']
            print sid
            send_ret = self.send(sid, phone, message)
            print send_ret
            ret_id = int(send_ret['errno'])
            print ret_id
            if ret_id == 0:
                return self.__ret(env, start_response, 0, 'Message Commit ok')
            elif ret_id == -1:
                return self.__ret(env, start_response, 9, 'Error: Unknow message encoding')
            elif ret_id == -2:
                return self.__ret(env, start_response, 8, 'Error: your account have not enough money')
            elif ret_id == -3:
                return self.__ret(env, start_response, 10, 'Error: No message to send')
            elif ret_id == -4:
                return self.__ret(env, start_response, 11, 'Error: Message char count is too large')
            elif ret_id == -5:
                return self.__ret(env, start_response, 12, 'Error: The phone number count is larger than 1000')

        except:
            print_exc();
            return self.__ret(env, start_response, 1, 'Error: send error')
    def check_user_pass(self, user, password):
        user_uid, remain, postfix = self.__check_user(user, password, 'normal')
        if user_uid == None:
            return -1
        elif remain < 1:
            return -2
        return 0


    def send(self, sid, phone, message):
        params = json.dumps({'q': 'sendmessage',
                                   'sid':sid,
                                   'address':phone,
                                   'msg':message
        })
        headers = {"Content-type": "application/x-www-form-urlencoded",
                           "Accept": "text/plain"}
        conn = httplib.HTTPConnection(smsd_url, smsd_port)
        conn.request("POST", "", params, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        d = json.loads(data)
        return d

    def auth(self, username, password):
        params = json.dumps({'q': 'auth',
                                   'user': username,
                                   'pass': sha1(password).hexdigest(),

        })
        headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
        conn = httplib.HTTPConnection(smsd_url, smsd_port)
        conn.request("POST", "", params, headers)
        res = conn.getresponse()
        data = res.read()
        d = json.loads(data)
        conn.close()
        return d

    def __ret(self, env, start_response, errno, message = None):
        self.logger.debug('return: %d, %s' % (errno, message))
        start_response('200 OK', [('Content-type', 'text/plain')])
        if self.cfg.sendsms.verbose > 0 and message != None:
            return ['%d,%s' % (errno, message)]
        elif errno > 0:
            return ['%d,%d,message commit success' % (1, errno)]
        else :
            return ['%d' % (errno)]
    

    def __check_user(self, u, p,type):
        password = p
        if type == 'normal':
            password = sha1(p).hexdigest()
            
        ret = self.db.raw_sql_query('SELECT uid,msg_num,msg_postfix FROM user WHERE username = %s AND password = %s AND can_post = TRUE AND need_check = FALSE',
                                    (u, password))
        if len(ret) == 0:
            return None, None, None
        user_uid, msg_num, msg_postfix = ret[0]
        pending = self.db.raw_sql_query('SELECT SUM(msg_num) FROM message WHERE user_uid = %s AND status = %s',
                                        (user_uid, message.F_ADMIT))[0][0]
        return user_uid, msg_num - (pending or 0), msg_postfix

def wsgiref_daemon():
    port = 8081
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, sendsms2(using_wsgiref = True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    smsd_url = 'localhost'
    smsd_port = '8082'
    wsgiref_daemon()
else:
    application = sendsms2(conf = smsd_path + '/smsd.ini')
