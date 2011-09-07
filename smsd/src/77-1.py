import threading
import time
import socket
import struct
import MySQLdb
import logging
import sys
import xml.dom.minidom

xmldom = xml.dom.minidom.parse("config.xml")
configdom = xmldom.getElementsByTagName('config')[0]
db_host = configdom.getElementsByTagName("db_host")[0].childNodes[0].data
db_port = int(configdom.getElementsByTagName("db_port")[0].childNodes[0].data)
db_name = configdom.getElementsByTagName("db_name")[0].childNodes[0].data
db_user = configdom.getElementsByTagName("db_user")[0].childNodes[0].data
db_passwd = configdom.getElementsByTagName("db_passwd")[0].childNodes[0].data
db_charset = configdom.getElementsByTagName("db_charset")[0].childNodes[0].data
log_file_path = configdom.getElementsByTagName("logfile")[0].childNodes[0].data
socket_ip = configdom.getElementsByTagName("socket_ip")[0].childNodes[0].data
socket_port = int(configdom.getElementsByTagName("socket_port")[0].childNodes[0].data)

logging.basicConfig(filename=log_file_path, level=logging.INFO, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')
logging.info('Begin start..')

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

def reconn_mysql():
    while True:
        try:
            conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_passwd, db=db_name, charset=db_charset)
            logging.info("Mysql retry connection success")
            break
        except MySQLdb.Error, e:
            logging.info("Mysql retry connection error")
            time.sleep(10)
    return conn
#socket reconn
def reconn_socket():
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
            logging.info('Socket Connection Success')
            t1 = threading.Thread(target=thread_sumbit_sms, name="sumbit_sms", args=(clisock,))
            t2 = threading.Thread(target=thread_recv_resp, name="recv_resp", args=(clisock,))
            t1.start()
            t2.start()
    except Exception, e:
        print e
        logging.error(e)

def thread_sumbit_sms(clisock):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_passwd, db=db_name, charset=db_charset)
    cursor = conn.cursor()
    print "Sumbit sms thread mysql connect success!"
    logging.info(" Sumbit sms thread connect to mysql success!")
#    while True:
#        try:
#            sqlstr = "select sequence_id,caller,called,sm_content from smpp_send_"+str(time.strftime('%Y%m',time.localtime(time.time())))+" where status = -2 and sche_send_time <= now()"
#            n = cursor.execute(sqlstr)
#            if(n>0):
#                for row in cursor.fetchall():
#                    seqence_id = row[0]
#                    caller = str(row[1])
#                    called = str(row[2])
#                    sm_content = str(row[3])
#                    msg_body = pack_sm_msg(seqence_id, caller, called, sm_content)
#                    try:
#                        clisock.send(msg_body)
###                      cursor.execute("update smpp_send set status = -1 where sequence_id = %s",seqence_id)
#                        sqlstr = "update smpp_send_"+str(time.strftime('%Y%m',time.localtime(time.time())))+" set status = -1 where sequence_id = %s"
#                        cursor.execute(sqlstr,seqence_id)
#                        conn.commit()
#                    except socket.error,e:
#                        logging.error("socket error,try to reconnection..")
#                        conn.close()
#                        return "0"
#            else:
#                logging.info("no data")
#                time.sleep(10)
#        except MySQLdb.Error, e:
#            if e[0]==2006:
#                logging.info(e)
#                conn = reconn_mysql()
#                cursor = conn.cursor()
#            elif e[0]==1103:
#                logging.info(e)


    send_msg = pack_sm_msg(1111111, "18906413323", "18616820727", "test")
    clisock.send(send_msg)


def thread_recv_resp(clisock):
#    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_passwd, db=db_name, charset=db_charset)
#    cursor = conn.cursor()
    print "Recv sms response thread mysql connect success!"
    logging.info(" Recv sms response thread connect to mysql success!")
    while True:
        try:
            resp_buffer = clisock.recv(1024)
            if(len(resp_buffer) > 0):
                bind_resp = unpack_resp(resp_buffer)
                if(bind_resp != ""):
                    sequnce_id = bind_resp[3]
                    if(sequnce_id > 0):
                        print sequnce_id
#                        try:
#                            sqlstr = "update smpp_send_" + str(time.strftime('%Y%m', time.localtime(time.time()))) + " set status = 0 where sequence_id = %s"
#                            cursor.execute(sqlstr, sequnce_id)
#                            conn.commit()
#                        except MySQLdb.Error, e:
#                            if e[0] == 2006:
#                                logging.info(e)
#                                conn = reconn_mysql()
#                                cursor = conn.cursor()
#                            elif e[0] == 1103:
#                                logging.info(e)


        except socket.error, e:
            conn.close()
            logging.error("Socket connect error!")
            break
def main():
    pass
if __name__ == '__main__':
    main()
    #
    while True:
        try:
            clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clisock.connect((socket_ip, socket_port))
            
            system_id = "chen"
            passwd = "chen"
            system_type = ""
            bind_msg = bind_transmitter_msg(system_id, passwd, system_type)
            clisock.send(bind_msg)
            bind_resp_buffer = clisock.recv(1024)
            bind_resp = unpack_resp(bind_resp_buffer)
            print bind_resp
            if(bind_resp[2] == 0):
                logging.info('Socket Connection Success')
                t1 = threading.Thread(target=thread_sumbit_sms, name="sumbit_sms", args=(clisock,))
                t2 = threading.Thread(target=thread_recv_resp, name="recv_resp", args=(clisock,))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            else:
                print "Socket auth error"
                logging.error("Socket auth error!")
                sys.exit()
        except Exception, e:
            print e
            logging.error(e)
            time.sleep(30)
