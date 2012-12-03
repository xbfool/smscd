__author__ = 'xbfool'

# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8


from loadcfg import loadcfg
from dbsql import dbsql

import logging
import logging.handlers

import sys
import os
from os import makedirs
if __name__ != '__main__':
    smsd_path = os.path.dirname(__file__)
    #smsd_path = 'C:\\xampp\\htdocs\\smsd\\src'
    sys.path.append(smsd_path)

from utils import urldecode



def get_field_from_xml(xml, s):
    s1 = '<' + s + '>'
    s2 = '</' + s + '>'
    return xml[xml.find(s1) + len(s1):xml.find(s2)]
class sendsms(object):
    def __init__(self, conf='smsd.ini', using_wsgiref=False):
        if not using_wsgiref:
            print '%s instance created, id 0x%08x' %\
                  (self.__class__.__name__, id(self))
        self.num_req = 0
        self.cfg = loadcfg(conf)
        self.db = dbsql(**self.cfg.database.raw_dict)
        LOG_FILENAME = '/tmp/logs/smsd.honglian606.log'
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
        print '%s instance 0x%08x destroyed, %d request(s) processed' %\
              (self.__class__.__name__, id(self), self.num_req)

    def __call__(self, env, start_response):
        # request handler

        self.logger.debug('%s', env['QUERY_STRING'])

        ret = 0
        return self.__ret(env, start_response, ret)


    def __ret(self, env, start_response, errno, message=None):
        start_response('200 OK', [('Content-type', 'text/plain')])

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
