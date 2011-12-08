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

def pack_sm_msg(sequence_no, caller, called, msg_content):
    command_id = 4
    command_status = 0
    server_type = "0"
    source_addr_ton = '1'
    source_addr_npi = '1'
    dest_address_ton = '1'
    dest_addr_npi = '1'
    source_address = caller
    esm_class = '0'
    protocol_ID = '0'
    priority_flag = '0'
    schedule_delivery_time = ""
    validity_peroid = ""
    registered_delivery = '0'
    replace_if_present_flag = '0'
    data_coding = '8'
    sm_default_msg_id = '0'
    sm_length = chr(len(msg_content))
    msg_fmt = "!iiii" + str(len(server_type)) + "sxcc" + str(len(caller)) + "sxcc" + str(len(called)) + "sxccc" + str(len(schedule_delivery_time)) + "sx" + str(len(validity_peroid)) + "sxccccc" + str(len(msg_content)) + "sx"
    msg_len = struct.calcsize(msg_fmt)
    print msg_len
    msg_send = struct.pack(msg_fmt, msg_len, command_id, command_status, sequence_no, server_type, source_addr_ton, source_addr_npi, caller, dest_address_ton, dest_addr_npi, called, esm_class, protocol_ID, priority_flag, schedule_delivery_time, validity_peroid, registered_delivery, replace_if_present_flag, data_coding, sm_default_msg_id, sm_length, msg_content)
    return msg_send

def recv_resp(clisock):
    try:
        clisock.settimeout(5)  
        resp_buffer = clisock.recv(1024)
        if(len(resp_buffer) > 0):
            bind_resp = unpack_resp(resp_buffer)
            print "bind_resp: ", bind_resp
            if(bind_resp != ""):
                sequnce_id = bind_resp[3]
                if(sequnce_id > 0):
                    print "recv seq id: " , sequnce_id
                    return sequnce_id
        return 0
    except:
        print 'recv_timeout'
        return -1
               
class CardProtocol(Protocol):
        
    def connectionMade(self):
        print 'connectionMade'
        self.is_login = False
        self.seq = 0
        self.login()
        
    def login(self):
        print 'in login'
        bind_msg = bind_transmitter_msg('chen', 'chen', '')
        self.transport.write(bind_msg)
        
        
    def dataReceived(self, line):
        if not self.is_login:
            s = unpack_resp(line)
            if s[2] == 0:
                print 'logged in ok'
                self.is_login = True
                self.sendsms('15314106299', '18616820727', 'test from sender4')
            else:
                print 'logged in failed'
        else:
            bind_resp = unpack_resp(line)
            if(bind_resp != ""):
                sequnce_id = bind_resp[3]
                if(sequnce_id > 0):
                    print "recv seq id: " , sequnce_id
                    return sequnce_id
                
    def sendsms(self, card, to, msg):
        print 'sending sms from %s, to %s, msg: %s' % (card, to, msg)
        self.seq += 1
        to_send = pack_sm_msg(self.seq, card, to, msg)
        self.transport.write(to_send)
        
class CardFactory(ReconnectingClientFactory):
    protocol = CardProtocol
    def buildProtocol(self, addr):
        self.resetDelay()
        return self.protocol()
def gotProtocol(p):
    print 'abc'
    p.sendMessage()

point = TCP4ClientEndpoint(reactor, '219.146.6.136', 5208)
d = point.connect(CardFactory())
d.addCallback(gotProtocol)
reactor.run()

