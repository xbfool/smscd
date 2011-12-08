from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol, Factory, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols.basic import LineReceiver
import struct
def bind_transmitter_msg(system_id, passwd, system_type):
    command_id = 2
    command_status = 0
    sequence_no = 1
    interface_version = '0'
    ton = '0'
    npi = '0'
    address_range = ""
    msg_fmt = "!iiii" + str(len(system_id)) + "sx" + str(len(passwd)) + "sxxcccx"
    print msg_fmt
    msg_len = struct.calcsize(msg_fmt)
    print msg_len
    command_body = struct.pack(msg_fmt, msg_len, command_id, command_status, sequence_no, system_id, passwd, interface_version, ton, npi)
    return command_body
    
def unpack_resp(msg_recv):
    msg_fmt = "!iiii"
    str_len = len(msg_recv) - struct.calcsize(msg_fmt)
    msg_fmt = msg_fmt + str(str_len) + "s"
    try:
        msg_body = struct.unpack(msg_fmt, msg_recv)
    except:
        logging.error("unpack resp error")
        logging.error(repr(msg_recv))
        msg_body = ""
    return msg_body
    
class CardProtocol(Protocol):
    
    def connectionMade(self):
        self.login()
        
    def login(self):
        bind_msg = bind_transmitter_msg('chen', 'chen', '')
        self.transport.write(bind_msg)
        print 'haha'
        
    def dataReceived(self, line):
        print len(line)
        s = unpack_resp(line)
        print s
        
class CardFactory(ReconnectingClientFactory):
    protocol = CardProtocol
    def buildProtocol(self, addr):
        self.resetDelay()
        return self.protocol()
def gotProtocol(p):
    print 'abc'
    p.sendMessage()

reactor.connectTCP('219.146.6.136', 5208, CardFactory())
reactor.run()
