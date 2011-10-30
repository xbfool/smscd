# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from Queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime, timedelta
from time import sleep


from zhttp import zhttp_pool
import time
from random import seed, shuffle
from settings import sender_settings

from msg_util import MsgController
from traceback import print_exc, format_exc
import logging
import logging.handlers
from msg_status import channel_status
from os import makedirs
class sms_sender(object):
    def __init__(self, chk_interval=30):
        self.__chk_interval = chk_interval

        self.msg_controller = MsgController()
        self.settings = sender_settings().settings
        self.timeout_dict = {}
        self.err_msg_dict = {}
        self.chanel_name_id_dict = {}
        LOG_FILENAME = './logs/smsd.sender.log'
        try:
            makedirs('./logs')
        except:
            pass
        # Set up a specific logger with our desired output level
        my_logger = logging.getLogger('smsd.sender')
        my_logger.setLevel(logging.DEBUG)
        # Add the log message handler to the logger

        handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=10000000, backupCount=100)
        my_logger.addHandler(handler)
        
        handler.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # add formatter to ch
        handler.setFormatter(formatter)


        self.logger = my_logger
        
        self.__zhttp_pool = zhttp_pool(1, self.settings, self.__http_callback, timeout_callback=self.__timeout_callback)
        

        self.__ret_queue = Queue(0x10000)
        
        self.__pending = []
        self.timeout_time = 1800
        self.__worker_exit_lock = Lock()
        self.__worker_exit_lock.acquire()
        self.__worker_thread = Thread(None, self.__worker, '%s checker thread' % self.__class__.__name__)
        self.__worker_thread.start()

    def stop(self):
        self.__zhttp_pool.stop()
        self.__worker_exit_lock.release()
        self.__worker_thread.join()
    
       
    def __http_callback(self, param, ret):
        # CAUTION: must thread safe
        self.__ret_queue.put((param, ret))
    def __timeout_callback(self, param, ret):
        pass
        
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
        while True:
            try:
                param, ret = self.__ret_queue.get(False)
            except Empty:
                # print '%s: no response yet' % self.__class__.__name__
                break
            print '%d, %s' % (param['uid'], ret)
            if ret == None:
                #here means the channel is down, nothing returned
                try:
                    self.logger.debug('connection error: this msg:%s connection error' % (param)) 
                    item = self.chanel_name_id_dict[param['setting']['name']]
                    if self.timeout_dict.get(item['uid']) and self.timeout_dict[item['uid']]['count'] >= 6:
                        self.msg_controller.down_channel(item, param['msg']['address'][0:11])
                        self.logger.debug('channel down: channel:%s' % (item))
                    else:
                        if not self.timeout_dict.get(item['uid']):
                            self.timeout_dict[item['uid']] = {'count':0, 
                                                              'last_update':datetime.now()}
                                                        
                        self.timeout_dict[item['uid']]['count'] += 1
                        self.logger.debug('channel error: this channel:%s is the %d times down' % (item['name'], 
                                                                                            self.timeout_dict[item['uid']]['count']))
                        self.timeout_dict[item['uid']]['last_update'] = datetime.now()
                except:
                    print_exc()

              
            try:
                if param['setting'] != None and param['setting'].get('process_ret'):
                    process = param['setting']['process_ret']
                    param['time'] = now
                    param['ret'] = ret
                    self.logger.debug('processing ret : param:%s' %(param))
                    ret = 0
                    try:
                        ret = process(self, param)
                    except:
                        pass
                    
                    if ret == 1:
                        if self.err_msg_dict.get(param['uid']):
                            del self.err_msg_dict[param['uid']]
                    elif self.err_msg_dict.get(param['uid']):
                        item = self.err_msg_dict.get(param['uid'])
                        item[param['setting']['name']] = 1
                        if len(item) >= 3:
                            self.msg_controller.send_fail(param, 'this message send fail more than 3 times')
                            self.logger.debug('msg error: this msg is error for some reason %s' % (param)) 
                            del self.err_msg_dict[param['uid']]
                    else:
                        item = {}
                        self.err_msg_dict[param['uid']] = item
                        item[param['setting']['name']] = 1
            except:
                pass
        
            try:
                self.__pending.remove(param['uid'])
            except:
                print '%s: CAUTION, uid %d does NOT exist in __pending' \
                % (self.__class__.__name__, param['uid'])
    
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
                continue
            msg['addr'] = msg['address'].split(';')
            channel_list = self.msg_controller.get_channel_list(msg)
            if len(channel_list) == 0:
                continue
            
            for item in channel_list:
                #add for check process_ret, awlsome design
                if item['name'] not in self.chanel_name_id_dict:
                    self.chanel_name_id_dict[item['name']] = item
                    
                #if channel stop means there is some thing error in our system
                #don't neet to try
                if channel_status.is_channel_stop(item['status'], msg['addr'][0]):
                    self.logger.debug('channel error: this channel:%s is down' % (item['name'])) 
                    continue
                
                #channel ok but in timeout dict means cannot cannot connet for last try
                #when last_update >= time interval than could have a try again
                elif (channel_status.is_channel_ok(item['status'], msg['addr'][0]) and self.timeout_dict.get(item['uid']) and
                      datetime.now() - self.timeout_dict[item['uid']]['last_update'] <= timedelta(seconds=self._getWaitTime(self.timeout_dict[item['uid']]['count']))):
                    continue
                
                #if tried a lot of times then the channel is down for some time
                #retry it 2 hour later                                                               
                elif (self.timeout_dict.get(item['uid']) and 
                      datetime.now() - self.timeout_dict[item['uid']]['last_update'] <= timedelta(hours=2) and
                    not channel_status.is_channel_ok(item['status'], msg['addr'][0])):
                    continue
                #not a good message, no need to try
                elif self.err_msg_dict.get(msg['uid']) and item['setting']['name'] in self.err_msg_dict[msg['uid']]:
                    continue
                
                
                try:
                    self.__pending.append(msg['uid'])
                    msg['channel'] = item['name']

                    if not channel_status.is_channel_ok(item['status'], msg['addr'][0]):
                        if self.timeout_dict.get(item['uid']):
                            del self.timeout_dict[item['uid']]
                        self.msg_controller.start_channel(item, msg['addr'][0])
                        self.logger.debug('channel start: channel:%s' % (item))
                    sending_str = 'sending : msg_uid:%s, channel:%s, msg:%s' % (msg['uid'], item['setting'], msg)
                    self.logger.debug(sending_str)
                    print sending_str
                    item['setting']['process_req'](self.__zhttp_pool, item['setting'], msg)
                    #here just means our function not error, not means the channel not error
                    count += 1
                    break
                except:
                    if msg['uid'] in self.__pending:
                        del self.__pending[msg['uid']]
                    count += 1
                    print_exc()
                    #this means our process_req has some error
                    #no need to try, stop the channel
                    self.logger.debug('sending error: msg_uid:%s, channel:%s, msg:%s' % (msg['uid'], item['setting'], msg))
                    self.logger.debug('sending exception: \n %s' % format_exc())
                    
                    self.msg_controller.stop_channel(item, msg['addr'][0])

                
        return count

    def _getWaitTime(self, count):
        if count <= 0:
            return 0
        elif count == 1:
            return 5
        elif count == 2:
            return 10
        elif count == 3:
            return 20
        elif count == 4:
            return 30
        elif count == 5:
            return 60
        elif count == 6:
            return 120
        else:
            return 3600

if __name__ == '__main__':
    sender = sms_sender()
    
    while True:
        time.sleep(10)
    sender.stop()
