__author__ = 'xbfool'
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
class Messagecount(object):
    def __init__(self, conf = 'smsd.ini', using_wsgiref = False):
        if not using_wsgiref:
            print '%s instance created, id 0x%08x' %\
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
        print '%s instance 0x%08x destroyed, %d request(s) processed' %\
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
            return self.__ret(env, start_response, -1, 'Error: username is empty')
        if password is None:
            return self.__ret(env, start_response, -2, 'Error: password is empty')

        user_pass_ret = self.check_user_pass(username, password)
        if user_pass_ret == -1:
            return self.__ret(env, start_response, -3, 'Error: username and password not match')
        else:
            return self.__ret(env, start_response, user_pass_ret)


    def check_user_pass(self, user, password):
        user_uid, remain, postfix = self.__check_user(user, password, 'normal')
        if user_uid == None:
            return -1
        else:
            return remain
        return 0

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
    httpd = make_server('', port, Messagecount(using_wsgiref = True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    smsd_url = 'localhost'
    smsd_port = '8082'
    wsgiref_daemon()
else:
    application = Messagecount(conf = smsd_path + '/smsd.ini')
