# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from traceback import print_exc
from hashlib import sha1
import sys
if __name__ != '__main__':
    smsd_path = '/home/jimmyz/smsd/src'
    #smsd_path = 'C:\\xampp\\htdocs\\smsd\\src'
    sys.path.append(smsd_path)

from utils import urldecode
from loadcfg import loadcfg
from dbsql import dbsql

from message import message

class querymessage(object):
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

          
        if username == None or username == '':
            return self.__ret(env, start_response, -99, 'invalid query, no user')
        if password == None or password == '':
            return self.__ret(env, start_response, -99, 'invalid query, no pass')
  
        user_uid, remain = self.__check_user(username, password)
        if user_uid == None:
            return self.__ret(env, start_response, -1, 'user not exist or wrong pass')
        else:
            return self.__ret(env, start_response, remain, 'the num return is the message count remain')
        
    def __ret(self, env, start_response, errno, message = None):
        start_response('200 OK', [('Content_type', 'text/plain')])
        if self.cfg.sendsms.verbose > 0 and message != None:
            return ['%d,%s' % (errno, message)]
        elif errno > 0:
            return ['%d,%d,message commit success' % (1, errno)]
        else :
            return ['%d' % (errno)]
    

    def __check_user(self, u, p):
        ret = self.db.raw_sql_query('SELECT uid,msg_num FROM user WHERE username = %s AND password = %s AND can_post = TRUE AND need_check = FALSE',
                                    (u, sha1(p).hexdigest()))
        if len(ret) == 0:
            return None, None
        user_uid, msg_num = ret[0]
        pending = self.db.raw_sql_query('SELECT SUM(msg_num) FROM message WHERE user_uid = %s AND status = %s',
                                        (user_uid, message.F_ADMIT))[0][0]
        return user_uid, msg_num - (pending or 0)
    

        

def wsgiref_daemon():
    port = 8080
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, querymessage(using_wsgiref = True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    wsgiref_daemon()
else:
    application = querymessage(conf = smsd_path + '/smsd.ini')
