from webtest import TestApp
def debug_app(env, resp):
    resp(
     '200 OK', [('Content-type', 'text/html')])
    print env['PATH_INFO'].split('/')
    return ['<h1>Hello, World!</h1>']

app = TestApp(debug_app)
res = app.get('/index.html')
print res.status
print res.body