import twisted.internet
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.resource import Resource
from smsd_mod import smsd
    
def twisted_daemon(app, port = 80):
    import sys

    if sys.platform == 'linux2':
        from twisted.internet import epollreactor
        epollreactor.install()
        

    print 'using %s' % reactor.__class__.__name__
    
    res = WSGIResource(reactor, reactor.getThreadPool(), app)
    
    root = Resource()
    root.putChild('smsd', res)
    
    site = Site(root)
    reactor.listenTCP(port, site)
    reactor.run()
    
if __name__ == '__main__':
    twisted_daemon(smsd('smsd.ini', True), 8082)
    pass