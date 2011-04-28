'''
Created on 2010-9-5

@author: xbfool
'''

from hashlib import sha1
from datetime import date, datetime, timedelta
import time
from traceback import print_exc
import json

from utils import *

from loadcfg import loadcfg
from dbsql import dbsql
from dbobj import dbobj

class message(dbobj):
    table_name = 'message'
    fields = 'uid,user_uid,address,address_list,msg,msg_num,create_time,status,last_update,channel,fail_msg'
    key = 'uid'
    
    F_ALL = 0
    F_COMMIT = 1
    F_SEND = 2
    F_REJECT = 3
    F_ADMIT = 4
    F_DELETE = 5
    F_CANCEL = 6
    F_FAIL = 7
    F_POST_COMMIT = 8
    def __init__(self):
        self.uid = 0
        self.user_uid = 0
        self.address = ''
        self.address_list = 0
        self.msg = ''
        self.create_time = None
        self.status = 0
        self.last_update = None
        self.channel = 'default'
        self.msg_num = 0
        self.fail_msg = ''
        
    def new(self, user_uid, address, address_list, msg, status, channel):
        self.user_uid = user_uid
        self.address = address
        self.address_list = address_list
        self.msg = msg
        self.create_time = datetime.now()
        self.status = status
        self.last_update =  self.create_time
        self.msg_num = self.compute_num()
        self.channel = channel
        self.create()
        
    def from_row(self, uid, user_uid, address, address_list, msg, msg_num,
                 create_time, status, last_update, channel, fail_msg):
        self.uid = uid
        self.user_uid = user_uid
        self.address = address
        self.address_list = address_list
        self.msg = msg
        self.create_time = create_time
        self.status = status
        self.last_update =  last_update
        self.msg_num = msg_num    
        self.channel = channel
        self.fail_msg = fail_msg
            
    def compute_num(self):
        msgcontent = ""
        try:
            msgcontent = self.msg.decode('utf8')
        except:
            try:
                msg = self.msg.decode('gbk').encode('utf8')
                msgcontent = msg.decode('utf8')
            except:
                msgcontent = "'"
        p = 0
        if len(msgcontent) == 0:
            p = 0
        elif len(msgcontent) <= 70 and self.channel not in ('honglian_01',
                         'honglian_bjyh', 'honglian_jtyh',
                         'honglian_ty'):
            p = 1
        else:
            p = (len(msgcontent) - 1) / 64 + 1
        
        return len(self.address.split(';')) * p
        
    
    def change_status(self, status):
        self.status = status
        self.save('status')
    

    
    def to_json(self):
        d = {}
        try:
            d['uid'] = self.uid
            d['user_uid'] = self.user_uid
            d['username'] = ''
            d['address'] = self.address
            d['addr_num'] = len(self.address.split())
            d['address_list'] = self.address_list
            try:
                d['msg'] = self.msg.decode('utf8').encode('utf8')
            except:
                try:
                    d['msg'] = self.msg.decode('gbk').encode('utf8')
                except:
                    d['msg'] = 'unknown encoding'
            d['create_time'] = self.create_time.strftime("%y-%m-%d %H:%M")
            d['msg_num'] = self.msg_num
            d['status'] = self.status
            d['channel'] = self.channel
            if(self.last_update != None):
                d['last_update'] = self.last_update.strftime("%y-%m-%d %H:%M")
            else:
                d['last_update'] = self.create_time.strftime("%y-%m-%d %H:%M")
            d['fail_msg'] = self.fail_msg
        except:
            pass
        return d
