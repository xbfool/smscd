# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from traceback import print_exc
from hashlib import sha1
from datetime import datetime
import logging
import logging.handlers
import sys
from os import makedirs
if __name__ != '__main__':
    smsd_path = '/home/jimmyz/smsd/src'
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
    def __init__(self, conf='smsd.ini', using_wsgiref=False):
        if not using_wsgiref:
            print '%s instance created, id 0x%08x' % \
                (self.__class__.__name__, id(self))
        self.num_req = 0
        self.cfg = loadcfg(conf)
        self.db = dbsql(**self.cfg.database.raw_dict)
        LOG_FILENAME = '/tmp/logs/smsd.receiver_honglian.log'
        try:
            makedirs('/tmp/logs')
        except:
            pass
        my_logger = logging.getLogger('smsd.sender')
        my_logger.setLevel(logging.DEBUG)
        # Add the log message handler to the logger

        handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=10000000, backupCount=100)
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
        # request handler
        self.num_req += 1
        if env['REQUEST_METHOD'] != 'GET':
            return self.__ret(env, start_response, -99, 'invalid query, not GET')
        print env
        self.logger.debug('%s', env)
        try:
            query = urldecode(env['QUERY_STRING'])
            phone = query.get('phone')
            msgContent = query.get('msgContent')
            spNumber = query.get('spNumber')
            if len(spNumber) > 17:
                spNumber = spNumber[17:]
            time = datetime.now()
            self.db.raw_sql('INSERT INTO upload_msg(ext, number, content, time) VALUES(%s, %s, %s, %s)',
                    (spNumber, phone, msgContent, time))
        except:
            print_exc()
        ret = 0
        return self.__ret(env, start_response, ret)

        
    def __ret(self, env, start_response, errno, message=None):
        start_response('200 OK', [('Content_type', 'text/plain')])
        if self.cfg.sendsms.verbose > 0 and message != None:
            return ['%d,%s' % (errno, message)]
        elif errno > 0:
            return ['%d,%d,message commit success' % (1, errno)]
        else :
            return ['%d' % (errno)]
    
        

def wsgiref_daemon():
    port = 8080
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, sendsms(using_wsgiref=True))
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    wsgiref_daemon()
else:
    application = sendsms(conf=smsd_path + '/smsd.ini')
