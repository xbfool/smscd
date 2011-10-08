from wsgiref import simple_server

class PyRefWsgiEngine(object):
    def __init__(self, port, app):
        self.server = simple_server.make_server('', 8000, app)
    
    def run(self):
        self.server.serve_forever()
