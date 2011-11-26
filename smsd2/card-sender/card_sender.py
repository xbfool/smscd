'''
Created on 2011-11-19

@author: xbfool
'''
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory
from twisted.protocols import basic
import json
class CardSenderProtocol(basic.LineReceiver):
    def lineReceived(self, param):
        try:
            a = json.loads(param)
            self.transport.write('a good json string: %s\n' % param)
        except:
            self.transport.write('not a good json string: %s\n' % param)
        
        self.transport.loseConnection()

class CardSenderFactory(protocol.ServerFactory):
    protocol = CardSenderProtocol
    
    def __init__(self):
        pass

reactor.listenTCP(8888, CardSenderFactory())
reactor.run()