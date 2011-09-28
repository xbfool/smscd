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

def get_filtered_addr(addr, percent, my_seed):
    addr.sort()
    seed(my_seed)
    shuffle(addr)
    
    ret = addr[0:max(1, len(addr) * percent / 100)]
    return ret
class msg():
    def __init__(self):
        self.last_update = datetime.now()
        self.address_list = []
        self.address_pool = {}
        self.uid = ''
        self.msg = ''
        
class card_sender(object):
    def __init__(self, chk_interval=3):
        self.__chk_interval = chk_interval
        self.cfg = loadcfg('smsd.ini')
               
        self.__db = dbsql(**self.cfg.database.raw_dict)
        self.__dblock = Lock()
        self.__worker_exit_lock = Lock()
        self.__worker_exit_lock.acquire()
        self.__worker_thread = Thread(None, self.__worker, '%s checker thread' % self.__class__.__name__)   
        self.__worker_thread.start()      
        self.__message_send_pool = {}
        self.message_pool = {}
        self.seq_pool = {}
    def __process_queue(self):
        q = self.__db.raw_sql_query('SELECT user_uid, uid,address,msg,channel, msg_num, totaL_num, seed FROM message WHERE status = %s and channel = "send_card_a" ORDER BY uid DESC LIMIT 500',
                                     message.F_ADMIT)
        
        c = self.gen_card_messages(q)
        self.send_card_messages(c)
    def __worker(self):
        while not self.__worker_exit_lock.acquire(False):
            if self.__process_queue() == 0:
                sleep(self.__chk_interval)
        
    def stop(self):
        self.__worker_exit_lock.release()
        self.__worker_thread.join()
       
    def gen_card_messages(self, q):
        #TODO
        pass
    
    def send_card_messages(self, c):
        for item in c:
            self.send_card_message(item)
    
    def send_card_message(self, item):
        self.message_pool[item.uid] = item
        for addr in item.address_list:
            seq = self.genseqnum()
            self.send_message(seq, addr, msg)
            self.seq_pool[seq] = item.uid
            item.address_pool[seq] 
    
    def send_message(self):
        pass
    
    def genseqnum(self):
        if self.seqnum >= 1000000:
            self.seqnum = 1
        else:
            self.seqnum += 1
        return self.seqnum
if __name__ == '__main__':
    sender = card_sender()
    
    import time
    while True:
        time.sleep(10)
    sender.stop()
