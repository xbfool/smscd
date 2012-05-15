# -*- coding: utf-8 -*-
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def honglian_server(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)
    print 'abc'
    ret = ret_ok()
    return ret

def ret_ok():
    return '00'
    

def serve_honglian_server(port=8000):
    httpd = make_server('', port, honglian_server)
    print "Serving on port 8000..."
    httpd.serve_forever()
    
if __name__ == '__main__':
    serve_honglian_server()
    