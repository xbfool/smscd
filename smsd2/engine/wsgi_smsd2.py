# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8


import WsgiEngine
from smsd2.command.SmsdCommand import SmsdCommand
from smsd2.context.context import Context
from smsd2.database.create_table import create_table


class Smsd2(WsgiEngine.WsgiEngine):
    def __init__(self, env=None, start_response=None):
        WsgiEngine.WsgiEngine.__init__(self, env, start_response)
        self.c = Context('config.yaml')
        create_table(self.c.db)
        self.add_command(SmsdCommand(self.c), '/smsd', 'json')
        
        
def wsgiref_daemon():
    port = 8080
    from wsgiref.simple_server import make_server
    httpd = make_server('', port, Smsd2())
    print 'running wsgiref daemon on port: %d' % port
    httpd.serve_forever()

if __name__ == '__main__':
    wsgiref_daemon()
else:
    application = Smsd2()
