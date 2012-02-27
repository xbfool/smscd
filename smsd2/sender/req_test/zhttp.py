# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

# a simple wrapper around httplib
#    targeting connection reusing and simplified usage

# TODO: save cookies

from urllib import urlencode
from httplib import HTTPConnection
from threading import Thread, Lock
from Queue import Queue
from traceback import print_exc

class zhttp(object):
    def __init__(self, host, path='/', mode='POST', port=80, timeout=90, **kargs):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.path = path
        self.params = urlencode(kargs)
        self.send_eval = compile('self.send_%s(**kargs)' % mode, '<string>', 'eval')
        self.connect()
        
    def connect(self):
        self.conn = HTTPConnection(self.host, self.port, False, self.timeout)
        
    def close(self):
        self.conn.close()
    
    def send(self, **kargs):
        return eval(self.send_eval)
    
    def send_POST(self, path=None, **kargs):
        path = path or self.path
        #data = self.params + '&' + urlencode(kargs)
        data = urlencode(kargs)
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        self.conn.request('POST', path, data, headers)
        res = self.conn.getresponse()
        return res.status, res.reason, res.read(), res.getheaders()

    def send_soap(self, path=None, soapaction=None, soap=None, port=80):
        # TODO: assemble soap here
        path = path or self.path
        headers = {"Content-type": "text/xml; charset=utf-8",
                   "SOAPAction": soapaction}
        self.port = port
        self.conn.request('POST', path, soap, headers)
        res = self.conn.getresponse()
        return res.status, res.reason, res.read(), res.getheaders()
    
    def send_GET(self, path=None, **kargs):
        # deprecated since url length is limited
        path = path or self.path
        path = path + '?' + self.params + '&' + urlencode(kargs)
        self.conn.request('GET', path)
        res = self.conn.getresponse()
        return res.status, res.reason, res.read()

class zhttp_wlock(zhttp):
    # use Lock as a member since Lock is a metaclass thus inherit from it is ugly
    def __init__(self, **kargs):
        self.__lock = Lock()
        zhttp.__init__(self, **kargs)
    
    def acquire(self, block=True):
        return self.__lock.acquire(block)
    
    def release(self):
        return self.__lock.release()

class zhttp_pool():
    __INVALID_ID = 0
    
    def __init__(self, thread_pool_size, host_settings, callback, retry=3, queue_length=0x10000, timeout_callback=None):
        self.__callback = callback
        self.__timeout_callback = timeout_callback
        self.__req_queue = Queue(queue_length)
        
        self.__retry_list = range(retry)
    
        # host_settings is a dict of connection settings, in other words, zhttp init parameters
        # caution, index must not be 0, since __INVALID_ID = 0
        self.__connection_pools = {}
        for i in host_settings:
            self.__connection_pools[i] = map(lambda a:zhttp_wlock(**host_settings[i]), (0,) * thread_pool_size)
            
        self.__thread_pool = map(
            lambda i:Thread(None, self.__worker, '%s thread %i' % (self.__class__.__name__, i)),
            range(thread_pool_size))
        map(lambda t:t.start(), self.__thread_pool)
        
    def req(self, setting_id, param_for_callback, **kargs):
        self.__req_queue.put((setting_id, param_for_callback, kargs))
    
    def stop(self):
        map(lambda t:self.__req_queue.put((self.__class__.__INVALID_ID, None, None)), self.__thread_pool)
        map(lambda t:t.join, self.__thread_pool)
    
    def __worker(self):
        current_sid = 0
        current_connection = None
        while True:
            # get request from the queue
            sid, param, kargs = self.__req_queue.get()
            if sid == self.__class__.__INVALID_ID:
                break
            if sid != current_sid:
                # we need to switch connection
                if current_sid != 0:
                    # release current connection if any
                    current_connection.release()
                for c in self.__connection_pools[sid]:
                    # find available connection by trying to acquire them in non-blocking mode
                    if not c.acquire(False):
                        continue
                    current_sid = sid
                    current_connection = c
                    break
                # since the connection pool is the same size of thread pool
                # there always will be an available connection, so i don't assert here
            ret = None
            for i in self.__retry_list:
                try:
                    ret = current_connection.send(**kargs)
                    self.__callback(param, ret)
                    break
                except:
                    print '%s: exception raised, reconnecting(%d)...' % (self.__class__.__name__, i)
                    print_exc()
                    current_connection.close()
                    current_connection.connect()
            else:
                self.__callback(param, ret)

def __dummy_callback(queue, ret):
    # caution the callback must be thread safe
    queue.put(ret)

def __selftest1():
    settings = {}
    settings['google'] = {'host': 'www.baidu.com', 'path' : '/s', 'mode' : 'GET'}
    settings['baidu'] = {'host': 'www.baidu.com', 'path' : '/s', 'mode' : 'GET'}
    
    p = zhttp_pool(3, settings, __dummy_callback)
    queries = ('python', 'google', 'baidu')
    ret = Queue() 
    for q in queries:
        p.req('google', ret, wd=q)
        p.req('baidu', ret, wd=q)
    p.stop()
    
    ret_list = []
    for i in range(6):
        ret_list.append(ret.get())
    pass

def __selftest0():
    h = zhttp(host='58.53.194.80',
              path='/swdx/services/APService',
              mode='soap')
    
    soap = \
'''
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <SendMessage xmlns="http://trust.me.nobody/cares/this/">
            <ApName>%s</ApName>
            <ApPassword>%s</ApPassword>
            <compcode>%s</compcode>
            <userCode>%s</userCode>
            <calledNumber>%s</calledNumber>
            <sendTime>%s</sendTime>
            <content>%s</content>
        </SendMessage>
    </soap:Body>
</soap:Envelope>
''' \
        % ('xghcdrs005', 'xu=qwe', 'xghcdrs1', 'xghcdrs05', '13436999640', '', 'test sms\n测试短信 \nfrom sender') 
        # % ('just', 'a', 'try', '!', '13436999640', '', 'tset sms\n测试短信 \nfrom sender') 
    ret = h.send(soapaction='http://58.53.194.80/swdx/services/APService/', soap=soap)
    print ret[0]
    print ret[1]
    print '\n'.join(map(str, ret[3]))
    print ret[2]
        
if __name__ == '__main__':
    __selftest0()
