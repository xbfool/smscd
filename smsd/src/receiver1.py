# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from traceback import print_exc
from hashlib import sha1
from datetime import datetime
import sys
import os
if __name__ != '__main__':
    smsd_path = os.path.dirname(__file__)
    #smsd_path = 'C:\\xampp\\htdocs\\smsd\\src'
    sys.path.append(smsd_path)

from utils import urldecode
from loadcfg import loadcfg
from dbsql import dbsql
from xml.dom.minidom import parseString
from message import message

def get_field_from_xml(xml, s):
    s1 = '<' + s + '>'
    s2 = '</' + s + '>'
    return xml[xml.find(s1) + len(s1):xml.find(s2)]
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
        
        print post_data
        try:
            corp_id = get_field_from_xml(post_data, 'corp_id')
            mobile = get_field_from_xml(post_data, 'mobile')
            ext = get_field_from_xml(post_data, 'ext')
            content = get_field_from_xml(post_data, 'content')
            content = content.decode('gbk').encode('utf8')
            time = get_field_from_xml(post_data, 'time')
            print mobile, ext, content, time
            self.db.raw_sql('INSERT INTO upload_msg(ext, number, content, time) VALUES(%s, %s, %s, %s)',
                        (ext, mobile, content, time))
        except:
            print_exc()
        ret = 0
        return self.__ret(env, start_response, ret)

        
    def __ret(self, env, start_response, errno, message = None):
        start_response('200 OK', [('Content-type', 'text/plain')])
        if self.cfg.sendsms.verbose > 0 and message != None:
            return ['%d,%s' % (errno, message)]
        elif errno > 0:
            return ['%d,%d,message commit success' % (1, errno)]
        else :
            return ['%d' % (errno)]
    
        

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
