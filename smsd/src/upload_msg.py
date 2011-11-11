# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from traceback import print_exc
from hashlib import sha1
from datetime import datetime
import json
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
from special_channel import *
class uploadmsg(object):
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
    def __ret_json(self, start_response, ret):
        start_response('200 OK', [('Content-type', 'application/json')])
        return [json.dumps(ret, separators=(',',':'), ensure_ascii=False)]
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
        start = query.get('start')
        end = query.get('end')
        maxnum = query.get('maxnum')
        
        max_num = 0
        start_dt = None
        end_dt = None
        passtype = query.get('passtype')
        
        if username == None or username == '':
            return self.__ret(env, start_response, -1, 'invalid query, no user')
        if password == None or password == '':
            return self.__ret(env, start_response, -2, 'invalid query, no pass')
        if start == None or start == '':
            return self.__ret(env, start_response, -3, 'invalid query, no start')
        if end == None or end == '':
            return self.__ret(env, start_response, -4, 'invalid query, no end')
        if maxnum == None or maxnum == '':
            max_number = 11
        else:
            max_number = int(maxnum)
        
        try:
            end_dt = datetime.strptime(end, '%Y%m%d%H%M%S')
            start_dt = datetime.strptime(start, '%Y%m%d%H%M%S')

        except:
            return self.__ret(env, start_response, -5, 'the time format is YYYYMMDDhhmmss')
        
        if passtype == None or passtype == '':
            passtype = 'normal'
        elif passtype == 'sha1':
            passtype = 'sha1'
        else:
            passtype = 'normal'
            
        user_uid, channels, ext = self.__check_user(username, password, passtype)
        
        if user_uid == None:
            return self.__ret(env, start_response, -1, 'user not exist or wrong pass')
        else:
            ret = self.__query(user_uid, channels, ext, start_dt, end_dt, max_number)
            return self.__ret_json(start_response, ret)

        
    def __ret(self, env, start_response, errno, message = None):
        start_response('200 OK', [('Content-type', 'text/plain')])
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
            
        ret = self.db.raw_sql_query('SELECT uid,channel_cm, channel_ct, channel_cu, ext FROM user WHERE username = %s AND password = %s',
                                    (u, password))
        if len(ret) == 0:
            return None
        user_uid, channel_cm, channel_ct, channel_cu, ext = ret[0]
        return user_uid, (channel_cm, channel_ct, channel_cu), ext
    
    def __query(self, u, channels, ext, start, end, num):
        ret = -1
        try:
            l = []
            d = self.db.raw_sql_query('SELECT ext, number, content, time FROM upload_msg WHERE ext = "%s" and time >= "%s" and time <= "%s" order by time limit %d' 
                                      % (ext, start, end, num))
            if d != None:
                for ext, number, content, time in d:
                    try:
                        content.decode('utf8')
                    except:
                        try:
                            content = content.decode('gbk').encode('utf8')
                        except:
                            pass
                    i = {'ext':ext, 'number':number, 'content':content, 'time':time.isoformat(' ')}
                    l.append(i)
            if len(l) >= num:
                return l
            self.special_channel_upload(channels, start, end, l, num - len(l))
 
        except:
            pass
        return l
        
        
    def special_channel_upload(self, channels, begin, end, l, maxnum):
        ext_numbers = special_channel(channels)
        for ext in ext_numbers:
            d = self.db.raw_sql_query('SELECT ext, number, content, time FROM upload_msg WHERE ext = "%s" and time >= "%s" and time <= "%s" order by time limit %d' % (ext, begin, end, maxnum))
            if d != None:
                for ext, number, content, time in d:
                    try:
                        content.decode('utf8')
                    except:
                        try:
                            content = content.decode('gbk').encode('utf8')
                        except:
                            pass
                    i = {'ext':ext, 'number':number, 'content':content, 'time':time.isoformat(' ')}
                    l.append(i)    
        return l


def wsgiref_daemon():
    port = 8080
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, uploadmsg(using_wsgiref = True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    wsgiref_daemon()
else:
    application = uploadmsg(conf = smsd_path + '/smsd.ini')
