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

import threading
import time
import socket
import struct
import logging
import sys
import xml.dom.minidom

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

def conn_socket():
    try:
        clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clisock.connect(('219.146.6.136', 5208))
        
        system_id = "chen"
        passwd = "chen"
        system_type = ""
        bind_msg = bind_transmitter_msg(system_id, passwd, system_type)
        clisock.send(bind_msg)
        bind_resp_buffer = clisock.recv(1024)
        bind_resp = unpack_resp(bind_resp_buffer)
        print bind_resp
        if(bind_resp[2] == 0):
            return clisock
        else:
            return None
    except Exception, e:
        print e
        return None
    
def sumbit_sms(clisock, seq_number, card_number, address, msg):
    print 'submit msg:', seq_number, card_number, address, msg
    send_msg = pack_sm_msg(seq_number, card_number, address, msg)
    clisock.send(send_msg)


def recv_resp(clisock):
    try:
        resp_buffer = clisock.recv(1024)
        if(len(resp_buffer) > 0):
            bind_resp = unpack_resp(resp_buffer)
            if(bind_resp != ""):
                sequnce_id = bind_resp[3]
                if(sequnce_id > 0):
                    print "bind_resp: ", bind_resp
                    print "recv seq id: " , sequnce_id
                    return sequnce_id

    except:
        return 0
