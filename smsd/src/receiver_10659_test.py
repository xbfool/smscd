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
import urllib
class sendsms(object):
    def __init__(self, conf = 'smsd.ini', using_wsgiref = False):
        if not using_wsgiref:
            print '%s instance created, id 0x%08x' % \
                (self.__class__.__name__, id(self))
        self.num_req = 0
    
    def __del__(self):
        print '%s instance 0x%08x destroyed, %d request(s) processed' % \
            (self.__class__.__name__, id(self), self.num_req)
        
    def __call__(self, env, start_response):
        # request handler
        self.num_req += 1
        try:
            print 'haha'
            #print urllib.unquote(env['QUERY_STRING']).decode('utf8')
        except:
            pass
        
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['1']

def wsgiref_daemon():
    port = 8888
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, sendsms(using_wsgiref = True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    wsgiref_daemon()
else:
    application = sendsms(conf = smsd_path + '/smsd.ini')
