#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ChannelException():
    pass
    
class ChannelClient():
    T_MOCK = 'mock'
    T_DUMB = 'dumb'
    T_NORMAL = 'normal'
    _types = (T_MOCK, T_DUMB, T_NORMAL)
    
    P_MOCK = 'mock'
    P_HONGLIAN = 'honglian'
    P_106A = '106a'
    _protocols = (P_MOCK, P_HONGLIAN, P_106A) 
    
    S_AVAILABLE = 'available'
    S_NO_CONNECTION = 'no_connection'
    S_NO_MONEY = 'no_money'
    S_SERVER_FAIL = 'server_fail'
    S_STOP_BY_MANAGER = 'stop_by_manager'
    
    _type = T_NORMAL
    _protocol = P_MOCK
    _status = S_AVAILABLE
    
    _id = 0
    _name = ''
    _desc = ''
    
    def __init__(self, id, name, desc='', channel_type=T_NORMAL, protocol=P_MOCK):
        self._id = id
        self._name = name
        self._desc = desc
        if channel_type in self._types: 
            self._type = channel_type
        else:
            self._type = self.T_MOCK
            
        if protocol in self._protocols:
            self._protocol = protocol
        else:
            self._protocol = self.P_MOCK
            
        self._status = self.S_STOP_BY_MANAGER
        
class ChannelCallback():
    @classmethod
    def send_success(cls, **args):
        print 'send_success'
        pass
        
    @classmethod
    def send_failed(cls, **args):
        print 'send_failed'
        pass
    
    @classmethod
    def channel_cannot_connect(cls, **args):
        print 'channel_cannot_connect'
        pass
    
    @classmethod
    def account_have_no_money(cls, **args):
        print 'account_have_no_money'
        pass
        
    @classmethod
    def addr_not_valid(cls, **args):
        print 'addr_not_valid'
        pass
    
    @classmethod
    def msg_not_valid(cls, **args):
        print 'msg_not_valid'
        pass
        