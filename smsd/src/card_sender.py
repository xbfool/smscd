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
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.sql import select
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
        self.init_db()

        self.init_card_pool()
        self.init_logger()
        self.kill_received = False
        
        self.card_socket = conn_socket()  
        if self.card_socket == None:
            raise Exception()
        self.__worker_exit_lock = Lock()
        self.__worker_exit_lock.acquire()
        self.__card_sender_lock = Lock()
        self.__sender_semaphone = threading.BoundedSemaphore(0)
        self.__worker_thread = Thread(None, self.__worker, '%s checker thread' % self.__class__.__name__)   
        self.__worker_thread.start() 
        
        self.__message_send_pool = {}
        self.message_pool = {}
        self.seq_pool = {}
        self.__pending = []
        self.__resp_thread = Thread(None, self.__resp_worker, '%s resp thread' % self.__class__.__name__)   
        self.__resp_thread.start()     


    def __process_queue(self):
        p = self.mysql_db.execute(select([self.msg_table],
                                         and_(self.msg_table.c.status == message.F_ADMIT,
                                         self.msg_table.c.channel == 'card_send_a')).\
                                  limit(100))

        c = self.gen_card_messages(p, self.msg_table)
        
        if c is None:
            return 0
        else:
            self.send_card_messages(c)
            return len(c)
        
    def __worker(self):
        while not self.__worker_exit_lock.acquire(False) and not self.kill_received:
            print 'checking queue: ', datetime.now()
            try:
                if self.__process_queue() == 0:
                    sleep(self.__chk_interval)
            except:
                print_exc()
        print 'exit send worker'    
    def __resp_worker(self):
        while not self.kill_received:
            if not self.__sender_semaphone.acquire(False):
                time.sleep(1)
                continue
            try:
                seq = recv_resp(self.card_socket)
                if(self.seq_pool.get(seq)):
                    uid = self.seq_pool[seq]
                    m = self.message_pool[uid]
                    address = m.address_pool[seq]
                    m.success_pool.add(seq)
                    last_update = datetime.now()
                    self.check_and_update_message(m)
            except:
                print_exc()
                self.card_socket = conn_socket() 
            if self.__card_sender_lock.locked(): 
                self.__card_sender_lock.release()
        print 'exit resp worker'
    def check_and_update_message(self, m):
        print 'in check_and_update_message'
        print len(m.success_pool), len(m.address_list)
        if len(m.success_pool) == len(m.address_list):
            self.set_message_success(m)
            self.__pending.remove(m.uid)
        
    def set_message_success(self, m):
        print 'send success'
        status = message.F_SEND
        result = 'card send success'
        try:
            self.mysql_db.execute(self.user_table.\
                                update().\
                                where(self.user_table.c.uid == m.user_uid).\
                                values({self.user_table.c.msg_num:self.user_table.c.msg_num - m.msg_num}))
            self.set_message_status(m, status, result)

            print 'successfull update'
        except:
            print_exc()
            print 'update error'

    
    def set_message_fail(self, m):
        status = message.F_FAIL
        result = 'card send fail'
        self.set_message_status(m, status, result)
    
    def set_message_status(self, m, status, result):
        try:
            self.mysql_db.execute(self.msg_table.\
                    update().\
                    where(self.msg_table.c.uid == m.uid).\
                    values({self.msg_table.c.status:status,
                            self.msg_table.c.last_update:m.last_update,
                            self.msg_table.c.fail_msg:result,
                            self.msg_table.c.sub_num:m.sub_num}))
        except:
            print_exc()
            pass
    def stop(self):
        self.__worker_exit_lock.release()
        self.__worker_thread.join()
        self.__resp_thread.join()
        print 'all thread join ok'
       
    def gen_card_messages(self, q, table):
        #TODO
        messages = []
        for item in q:
            if item[table.c.uid] in self.__pending:
                continue
            print item
            m = self.gen_card_message(item, table)
            if m is not None:
                messages.append(m)
                self.__pending.append(m.uid)
        return messages
    def get_user_percent(self, user_uid):
        r = self.mysql_db.execute(select(['user.percent'], self.user_table.c.uid == user_uid))
        return r.fetchone()[0]
    
    def gen_card_message(self, item, table):
        try:
            c = table.c
            percent = self.get_user_percent(item[table.c.user_uid])

            if percent == None or percent > 100:
                percent = 100
                
            address_list = item[c.address].split(';')
            if(percent is not None and percent <= 100 and percent >= 50 and item[c.total_num] >= 100):
                address_list = self.get_filtered_addr(address.split(';'), percent, item[c.seed])

            m = Msg()
            m.user_uid = item[c.user_uid]
            m.uid = item[c.uid]
            m.address_list = address_list
            m.msg = item[c.msg]
            m.msg_num = item[c.msg_num]
            m.sub_num = item[c.msg_num] * percent / 100
            if m.sub_num == 0 and [c.msg_num] != 0:
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
        self.__card_sender_lock.acquire()
        card_number = self.get_send_card_number()
        sumbit_sms(self.card_socket, seq, card_number, addr, msg)
        self.__sender_semaphone.release()
        self.logger.debug('time,%s,seq,%d,card,%s,addr,%s,msg,\'%s\'' % (str(datetime.now()), seq, card_number, addr, msg))
    
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
        self.cardpool.add_number_by_string('13376442584')
        self.cardpool.add_number_by_string('13376440784')
        self.cardpool.add_number_by_string('13376442504')
        self.cardpool.add_number_by_string('13376442714')
        self.cardpool.add_number_by_string('13376440764')
        
        self.cardpool.add_number_by_string('13376440934')
        self.cardpool.add_number_by_string('13376440914')
        self.cardpool.add_number_by_string('13376442374')
        self.cardpool.add_number_by_string('13376442704')
        self.cardpool.add_number_by_string('13376440694')

        self.cardpool.add_number_by_string('13376442394')
        self.cardpool.add_number_by_string('13376442344')
        self.cardpool.add_number_by_string('13376440804')
        self.cardpool.add_number_by_string('13376440554')
        self.cardpool.add_number_by_string('13376440924')

        self.cardpool.add_number_by_string('13376442674')
        self.cardpool.add_number_by_string('13376442894')
        self.cardpool.add_number_by_string('13376442094')
        self.cardpool.add_number_by_string('13376442524')
        self.cardpool.add_number_by_string('13376442384')

    
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
    def init_db(self):
        self.mysql_db = create_engine('mysql+mysqldb://%s:%s@localhost/%s' % 
                                      (self.cfg.database.user,
                                       self.cfg.database.passwd,
                                       self.cfg.database.db))
        
        from sqlalchemy.orm import sessionmaker
        self.meta = MetaData()
        try:
            self.msg_table = Table('message', self.meta, autoload=True, autoload_with=self.mysql_db)
            self.user_table = Table('user', self.meta, autoload=True, autoload_with=self.mysql_db)
        except:
            print_exc()
        Base.metadata.create_all(self.mysql_db) 
        Session = sessionmaker(bind=self.mysql_db)
        self.session = Session()
        
if __name__ == '__main__':
    sender = card_sender()
    
    import time
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            sender.kill_received = True
            break
    sender.stop()
    print 'all exit'
