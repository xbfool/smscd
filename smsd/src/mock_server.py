# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8


'''
Created on 2010-7-3

@author: xbfool
'''

from urlparse import parse_qs
from urllib import unquote, quote, urlencode
from hashlib import md5, sha1
from datetime import date, datetime, timedelta
from traceback import print_exc


def parse_query(str):
    query = parse_qs(str, True)
    # url-decode strings and do not care about multiple value on same key
    return dict(zip(query.keys(), map(lambda l:unquote(l[0]), query.values())))


class be(object):
    def __init__(self, using_wsgiref = False):
        self.user_id = "admin"
        self.passwd = "passwd"
        self.index = 0;
        
    def __call__(self, env, start_response):
        path = env.get('PATH_INFO', '').lstrip('/')
        query = parse_query(env.get('QUERY_STRING', ''))
        
        start_response('200 OK', [('Content-Type', 'text/plain')])
        self.index += 1
        try:
            u = query['uid']
            g = query['pwd']
            a = query['address']
            s = query['content']
            
            if u != self.user_id or g != self.passwd:
                ret = "<Reply errorCode='2'>login faild</Reply>"
            else:
                ret = "<Reply errorCode='1'>send ok</Reply>"
        except:
            ret = "<Reply errorCode='99'>request not valid</Reply>"
            pass

        return ret
          
def wsgi_daemon():
    from wsgiref.simple_server import make_server
    srv = make_server('', 8001, be(True))
    srv.serve_forever()

if __name__ == '__main__':
    wsgi_daemon()