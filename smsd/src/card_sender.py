'''
Created on 2011-9-22

@author: xbfool
'''
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from Queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
from time import sleep

from loadcfg import loadcfg
from dbsql import dbsql
from zhttp import zhttp_pool
from xml.dom.minidom import parseString
from xml.sax import saxutils
from message import message
from traceback import print_exc
from urlparse import urlparse
import urllib
import phonenumber
from struct import *
from hashlib import md5
from base64 import b64encode
from zlib import compress
from random import seed, shuffle
from card_channel import *
from sqlalchemy import create_engine
from cardpool import *

def get_filtered_addr(addr, percent, my_seed):
    addr.sort()
    seed(my_seed)
    shuffle(addr)
    
    ret = addr[0:max(1, len(addr) * percent / 100)]
    return ret
class Msg():
    def __init__(self):
        self.last_update = datetime.now()
        self.address_list = []
        self.address_pool = {}
        self.success_pool = set()
        self.uid = ''
        self.msg = ''
  
class card_sender(object):
    def __init__(self, chk_interval=3):
        self.__chk_interval = chk_interval
        self.cfg = loadcfg('smsd.ini')
        self.seqnum = 0
        self.__db = dbsql(**self.cfg.database.raw_dict)
        self.mysql_db = create_engine('mysql+mysqldb://%s:%s@localhost/%s' % 
                                      (self.cfg.database.user,
                                       self.cfg.database.passwd,
                                       self.cfg.database.db))
        from sqlalchemy.orm import sessionmaker
        Base.metadata.create_all(self.mysql_db) 
        Session = sessionmaker(bind=self.mysql_db)
        self.session = Session()
        
        self.__dblock = Lock()
        self.init_card_pool()
        self.init_logger()
        self.card_socket = conn_socket()  
        if self.card_socket == None:
            raise Exception()
        self.__worker_exit_lock = Lock()
        self.__worker_exit_lock.acquire()
        self.__worker_thread = Thread(None, self.__worker, '%s checker thread' % self.__class__.__name__)   
        self.__worker_thread.start() 

        self.__message_send_pool = {}
        self.message_pool = {}
        self.seq_pool = {}

        self.__resp_thread = Thread(None, self.__resp_worker, '%s resp thread' % self.__class__.__name__)   
        self.__resp_thread.start()     


    def __process_queue(self):
        q = self.__db.raw_sql_query('SELECT user_uid,uid,address,msg,seed,msg_num,total_num FROM message WHERE status = %s and channel = "card_send_a" ORDER BY uid DESC LIMIT 500',
                                     message.F_ADMIT)
        
        c = self.gen_card_messages(q)
        self.send_card_messages(c)

        if c is None:
            return 0
        else:
            return len(c)
        
    def __worker(self):
        while not self.__worker_exit_lock.acquire(False):
            if self.__process_queue() == 0:
                sleep(self.__chk_interval)
                
    def __resp_worker(self):
        while True:
            try:
                seq = recv_resp(self.card_socket)
                if(self.seq_pool.get(seq)):
                    uid = self.seq_pool[seq]
                    m = self.message_pool[uid]
                    address = m.address_pool[seq]
                    m.success_pool.add(address)
                    last_update = datetime.now()
                    self.check_and_update_message(m)
            except:
                print_exc()
                self.card_socket = conn_socket()  
    
    def check_and_update_message(self, m):
        print 'in check_and_update_message'
        print len(m.success_pool), len(m.address_list)
        if len(m.success_pool) == len(m.address_list):
            self.set_message_success(m)
        
    def set_message_success(self, m):
        print 'send success'
        status = message.F_SEND
        result = 'card send success'
        try:
            self.__db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                        (m.msg_num, m.user_uid))
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, m.last_update, result, m.sub_num, m.uid))
            print 'successfull update'
        except:
            print_exc()
            print 'update error'

    
    def set_message_fail(self, m):
        status = message.F_FAIL
        result = 'card send fail'
        try:
            self.__db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                        (status, m.last_update, result, m.sub_num, m.uid))
        except:
            pass
        
    def stop(self):
        self.__worker_exit_lock.release()
        self.__worker_thread.join()
        self.__resp_thread.join()
       
    def gen_card_messages(self, q):
        #TODO
        messages = []
        for user_uid, uid, address, msg, seed, msg_num, total_num in q:
            m = self.gen_card_message(user_uid, uid, address, msg, seed, msg_num, total_num)
            if m is not None:
                messages.append(m)
        return messages
                
    def gen_card_message(self, user_uid, uid, address, msg, seed, msg_num, total_num):
        try:
            user_percent = self.__db.raw_sql_query('SELECT percent FROM user WHERE uid = %s', user_uid)
            percent = user_percent[0][0]
            if percent == None or percent > 100:
                percent = 100
                
            address_list = address.split(';')
            if(percent is not None and percent <= 100 and percent >= 50 and total_num >= 100):
                address_list = self.get_filtered_addr(address.split(';'), percent, seed)

            m = Msg()
            m.user_uid = user_uid
            m.uid = uid
            m.address_list = address_list
            m.msg = msg
            m.msg_num = msg_num
            m.sub_num = msg_num * percent / 100
            if m.sub_num == 0 and msg_num != 0:
                m.sub_num = 1
            return m
        except:
            print_exc()
            return None
 
    def get_filtered_addr(self, addr, percent, my_seed):
        addr.sort()
        seed(my_seed)
        shuffle(addr)
        
        ret = addr[0:max(1, len(addr) * percent / 100)]
        return ret
    
    def send_card_messages(self, c):
        if c is None:
            return
        for item in c:
            self.send_card_message(item)
    
    def send_card_message(self, item):
        self.message_pool[item.uid] = item
        for addr in item.address_list:
            seq = self.genseqnum()
            self.send_message(seq, addr, item.msg)
            self.seq_pool[seq] = item.uid
            item.address_pool[seq] = addr
    
    def send_message(self, seq, addr, msg):
        card_number = self.get_send_card_number()
        sumbit_sms(self.card_socket, seq, card_number, addr, msg)
        self.logger.debug('time: %s, seq: %d,card: %s,addr: %s,msg: \'%s\'' % (str(datetime.now()), seq, card_number, addr, msg))
    
    def genseqnum(self):
        if self.seqnum >= 1000000:
            self.seqnum = 1
        else:
            self.seqnum += 1
        return self.seqnum
    
    def get_send_card_number(self):
        while True:
            n = self.cardpool.get_next_number()
            if n is None:
                time.sleep(10)
            else:
                self.session.commit()
                return n 
    def init_card_pool(self):
        self.cardpool = CardPool()
        self.cardpool.add_number_by_string('18906413323')
    
    def init_logger(self):
        import glob
        import logging
        import logging.handlers
        
        LOG_FILENAME = 'card_sender_log.out'
        
        # Set up a specific logger with our desired output level
        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(logging.DEBUG)
        
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME)
        
        my_logger.addHandler(handler)
        
        self.logger = my_logger
        
if __name__ == '__main__':
    sender = card_sender()
    
    import time
    while True:
        time.sleep(10)
    sender.stop()
