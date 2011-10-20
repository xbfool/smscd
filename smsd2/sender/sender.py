# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from Queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
from time import sleep


from zhttp import zhttp_pool
import time
from random import seed, shuffle
from settings import sender_settings
from ChannelController import ChannelController
from msg_util import MsgController
from traceback import print_exc
class sms_sender(object):
    def __init__(self, chk_interval=3):
        self.__chk_interval = chk_interval
        self.channel_controller = ChannelController()
        self.msg_controller = MsgController()
        self.settings = sender_settings().settings
        for item in self.settings.itervalues():
            item['timeout_count'] = 0
            item['last_update'] = datetime.now()
        
        self.__zhttp_pool = zhttp_pool(1, self.settings, self.__http_callback, timeout_callback=self.__timeout_callback)
        

        self.__ret_queue = Queue(0x10000)
        
        self.__pending = []
        self.timeout_time = 1800
        self.__timeout_lock = Lock()
        self.__worker_exit_lock = Lock()
        self.__worker_exit_lock.acquire()
        self.__worker_thread = Thread(None, self.__worker, '%s checker thread' % self.__class__.__name__)
        self.__worker_thread.start()

    def stop(self):
        self.__zhttp_pool.stop()
        self.__worker_exit_lock.release()
        self.__worker_thread.join()
    
    def __timeout_add(self, setting):
        self.__timeout_lock.acquire()
        setting['timeout_count'] += 1
        setting['last_update'] = datetime.now()
        self.__timeout_lock.release()
        
    def __check_channel_ok(self, setting):
        if setting['timeout_count'] <= 3:
            return True
        elif (datetime.now() - setting['last_update']).total_seconds() > self.timeout_time:
            self.__timeout_clean(setting)
            return True
        else:
            return False
    def __timeout_clean(self, setting):
        self.__timeout_lock.acquire()
        setting['timeout_count'] = 0
        setting['last_update'] = datetime.now()
        self.__timeout_lock.release()
        
    def __http_callback(self, param, ret):
        # CAUTION: must thread safe
        self.__ret_queue.put((param, ret))
    def __timeout_callback(self, param, ret):
        self.__timeout_add(param['setting'])
        
    def __worker(self):
        while not self.__worker_exit_lock.acquire(False):
            now = datetime.now()
            # process returns
            self.__process_ret(now)
            # process pending queue from database
            if self.__process_queue_new() == 0:
                #print '%s: no pending queue, sleep for %d seconds' % (self.__class__.__name__, self.__chk_interval)
                sleep(self.__chk_interval)
    

    def __process_ret(self, now):
        count = 0
        while True:
            try:
                param, ret = self.__ret_queue.get(False)
            except Empty:
                # print '%s: no response yet' % self.__class__.__name__
                break
            print '%d, %s' % (param['uid'], ret)
            try:
                self.__pending.remove(param['uid'])
            except:
                print '%s: CAUTION, uid %d does NOT exist in __pending' \
                % (self.__class__.__name__, param['uid'])
                
            try:
                if param['setting'] != None and param['setting'].get('process_ret'):
                    process = param['setting']['process_ret']
                    param['time'] = now
                    param['ret'] = ret
                    self.__timeout_clean(param['setting'])
                    count = count + process(self, param)
            except:
                pass
                
        if count > 0:
            self.__db.raw_commit()
    
    def get_filtered_addr(self, addr, percent, my_seed, total_num=0):
        if(percent is not None and percent <= 100 and percent >= 50 and total_num >= 100):
            addr.sort()
            seed(my_seed)
            shuffle(addr)
            
            ret = addr[0:max(1, len(addr) * percent / 100)]
            return ret
        else:
            return addr
        
    def __process_queue_new(self):
        messages = self.msg_controller.get_messages()
        count = 0
        self.msg_controller.clean_dict()
        for msg in messages:
            if msg['uid'] in self.__pending:
                print self.__pending
                continue
            self.__pending.append(msg['uid'])
            
            msg['addr'] = msg['address'].split(';')
            channel_list = self.msg_controller.get_channel_list(msg)
            print msg
            for item in channel_list:
                try:
                    msg['channel'] = item['name']
                    item['setting']['process_req'](self.__zhttp_pool, item['setting'], msg)
                    break
                except:
                    print_exc()
                    continue
                
            count += 1
        return count

                    

if __name__ == '__main__':
    sender = sms_sender()
    
    while True:
        time.sleep(10)
    sender.stop()
