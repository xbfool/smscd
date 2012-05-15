# -*- coding: utf-8 -*-
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def honglian_server(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    post_data = env['wsgi.input'].read(length)

    query = urldecode(post_data)
    
    username = query.get('username')
    password = query.get('password')
    epid = query.get('epid')
    
    start_response(status, headers)
    if (password != '123456' or 
        username != 'fdzxyy' or 
        epid != '6101'):
        ret = ret_password_error()
    else:
        
    return ret

def ret_ok():
    return '00'
    
def ret_password_error(user, pass):
    ret = 'error:用户名%s  密码错误%s' % (user, pass)
    return ret.decode('utf8').encode('gbk')

def serve_honglian_server(port=8000):
    httpd = make_server('', port, honglian_server)
    print "Serving on port 8000..."
    httpd.serve_forever()
    
if __name__ == '__main__':
    serve_honglian_server()
    