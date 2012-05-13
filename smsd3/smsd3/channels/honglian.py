# -*- coding: utf-8 -*-
import httplib, urllib
import copy
class ChannelCallback():
    def __init__(self):
        pass
        
    def bad_addr(self, channel, msg):
        print 'bad_addr: channel:%s, msg:%s' %\
         (channel.name, msg)
    
    def bad_msg(self, channel, msg):
        print 'bad_msg, channel:%s, msg:%s' %\
         (channel.name, msg)
        
    def parse_response(self, channel, msg, response):
        print 'bad_msg, channel:%s, msg:%s, response:%s' %\
         (channel.name, msg, response)
         
class ChannelHonglian():
    name = 'honglian'
    _sender = None
    _site = None
    _account = None
    _conn = None
    _retry_times = 3
    _callback = None
    def __init__(self, account, sender, callback, retry_times=3):
        self._sender = sender
        self._site = self.make_site()
        self._account = account
        self._retry_times = retry_times
        self._callback = callback

    
    def send(self, msg_uid, addr, msg):
        if not self.check_addr(addr):
            self._callback.bad_addr(self, msg_uid)
        if not self.check_msg(msg):
            self._callback.bad_msg(self, msg_uid)
            
        for i in range self._retry_times:
            try:
                response = self.raw_send(addr, msg)
                self._callback.parse_response(uid, response)
            except:
                self._sender.close()
                self._sender.connect()
        
        return self._callback.channel_error(self, uid)
    

    def raw_send(self, addr_list, msg_content):
        pass
               
    def compute_msg_num():
        pass
        
    def make_request(addr_list, msg_content):
        s = copy.copy(self._account)
        s['phone']=','.join(addr_list)
        s['message']='testhonglian'
        return s
        
        pass
    
    def parse_response():
        pass
        
    def make_site():
        return {
            'host': '219.238.160.81',
            'port': '80',
            'path': '/interface/limitnew.asp',
            'mode': 'POST',
        }
