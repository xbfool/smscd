from cherrypy import wsgiserver
from smsd2.engine.wsgi_smsd2 import Smsd2

server = wsgiserver.CherryPyWSGIServer(
            ('0.0.0.0', 8080), Smsd2(),
            server_name='localhost')
server.start()