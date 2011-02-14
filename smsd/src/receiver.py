'''
Created on 2010-10-20

@author: xbfool
'''
from Queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
from time import sleep

from loadcfg import loadcfg
from dbsql import dbsql
from zhttp import zhttp_pool, zhttp
from xml.dom.minidom import parseString
from xml.sax import saxutils
from message import message
from traceback import print_exc
from urlparse import urlparse
import urllib

class sms_receiver(object):
    def __init__(self, chk_interval = 10):
        self.__chk_interval = chk_interval
        self.cfg = loadcfg('smsd.ini')
        
        settings = {}
        
        settings['hlyd_01'] = {
            'name': 'hlyd_01',
            'host': 'hl.my2my.cn',
            'path': '/services/esmsservice',
            'mode': 'soap',
            'sub_mode': 'hlyd',
            'cpid': '9033',
            'cppwd': '123456',
            'process_ret' : sms_receiver.__process_ret_hlyd
        }
        self.settings = settings
        self.__zhttp_pool = zhttp_pool(1, settings, self.__http_callback)
        
        self.__db = dbsql(**self.cfg.database.raw_dict)
        self.__dblock = Lock()
        
        self.__ret_queue = Queue(0x10000)
        
        self.__pending = []
        self.req_id = 0
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
    
    def __worker(self):
        while not self.__worker_exit_lock.acquire(False):
            # process returns
            self.__process_ret()
            # process pending queue from database
            
            self.__process_queue()
            sleep(self.__chk_interval)

                
    def __process_ret_hlyd(self, param):
        try:
            resultDOM = parseString(param['ret'][2])
            result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.data
        
        
            print result
        except:
            status = message.F_FAIL
            pass
        pass
    def __process_ret(self):
        count = 0
        while True:
            try:
                param, ret = self.__ret_queue.get(False)
            except Empty:
                # print '%s: no response yet' % self.__class__.__name__
                break

            try:
                if param['setting'] != None and param['setting'].get('process_ret'):
                    process = param['setting']['process_ret']
                    param['ret'] = ret
                    count = count + process(self, param)
            except:
                pass
        if count > 0:
            self.__db.raw_commit()
    
    def __process_queue(self):
        self.__process_hualuyidong()

    
    def __process_hualuyidong(self):
        self.__pending.append(self.req_id)
        req_id = self.req_id
        self.req_id = self.req_id + 1
        setting =  self.settings['hlyd_01']
        soap = \
'''
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <getMoList xmlns="http://trust.me.nobody/cares/this/">
            <nextId>%s</nextId>
            <cpid>%s</cpid>
            <cppwd>%s</cppwd>
        </getMoList>
    </soap:Body>
</soap:Envelope>
''' \
        % ('3',
           setting['cpid'], setting['cppwd'])

        h = zhttp(host = 'hl.my2my.cn',
              path = '/services/esmsservice',
              mode = 'soap')
        ret = h.send(soapaction = 'http://hl.my2my.cn/services/esmsservice', soap = soap)
        print ret[2]
        try:
            resultDOM = parseString(ret[2])
            result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.data
        
            if result != '0':
                print result
        except:
            status = message.F_FAIL
            pass
        #print "processing"
        pass  
            
if __name__ == '__main__':
    receiver = sms_receiver()
    
    #from os import system
    #system('pause')
    
    import time
    while True:
        time.sleep(10)
    receiver.stop()
                