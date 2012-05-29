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

from common.log import logger

class user(dbobj):
    # dbobj need these
    table_name = 'user'
    fields = 'uid,description,username,password,parent_id,msg_num,flags,is_active,'\
    'create_time,last_login,can_weblogin,can_post,need_check,channel_cm,channel_cu,channel_ct,ext,'\
    'percent,msg_postfix'
    
    key = 'uid'
    # user right flags
    F_CHARGE                = 0x00000001 # right to charge msg_num to anybody
    F_CREATE_USER           = 0x00000002 # right to create child
    F_CREATE_CHARGE         = 0x00000004 
    
    def __init__(self):
        self.uid = 0 # uid stands for "unique id"
        self.username = ''
        self.description = ''
        self.password = ''
        self.parent_id = 0
        self.msg_num = 0
        self.flags = 0
        self.is_active = 0
        self.create_time = None
        self.last_login = None
        self.can_weblogin = False
        self.can_post = False
        self.need_check = True
        self.channel_cm = ''
        self.channel_cu = ''
        self.channel_ct = ''
        self.commit_num = 0
        self.children = {}
        self.ext = '' 
        self.percent = 100#sub numbers
        self.msg_postfix = ''
    #   self.logs = []
    #   self.commits = []
        
    def new(self, username, description, password, parent_id, msg_num, can_weblogin, 
            can_post, need_check, 
            channel_cm,
            channel_cu,
            channel_ct,flags = 0, percent = 100, msg_postfix = ''):
        """ new user """
        self.username = username
        self.description = description
        self.password = password
        self.parent_id = parent_id
        self.msg_num = msg_num
        self.flags = flags
        self.is_active = 1
        self.create_time = datetime.now()
        self.last_login = None
        self.can_weblogin = can_weblogin
        self.can_post = can_post
        self.need_check = need_check
        self.channel_cm = channel_cm
        self.channel_cu = channel_cu
        self.channel_ct = channel_ct
        self.percent = percent
        self.msg_postfix = msg_postfix
        self.create()
    
    def from_row(self, uid, description, username, password, parent_id, msg_num,
           flags, is_active, create_time, last_login, can_weblogin, can_post, need_check,
           channel_cm, channel_cu, channel_ct, ext, percent, msg_postfix):
        """ load from database """
        self.uid = uid
        self.username = username
        self.description = description
        self.password = password
        self.parent_id = parent_id
        self.msg_num = msg_num
        self.flags = flags
        self.is_active = is_active
        self.create_time = create_time
        self.last_login = last_login
        self.can_weblogin = can_weblogin
        self.can_post = can_post
        self.need_check = need_check
        self.channel_cm = channel_cm
        self.channel_cu = channel_cu
        self.channel_ct = channel_ct
        self.ext = ext
        self.percent = percent
        self.msg_postfix = msg_postfix
        
    def __auth(self, password):
        return self.password == password and self.is_active == 1
    
    def web_auth(self, password):
        return self.__auth(password) and self.can_weblogin
    
    def post_auth(self, password):
        return self.__auth(password) and self.can_post
    
    def change_weblogin_flag(self, flag):
        self.can_weblogin = flag
        
    def change_post_flag(self, flag):
        self.can_post = flag
    
    def change_check_flag(self, flag):
        self.need_check = flag
        
    def change_password(self, password):
        self.password = password
        self.save('password')
        
    def add_message(self, num):
        self.msg_num = self.msg_num + num
        self.save('msg_num')
        
    
    def set_status(self, status):
        self.is_active = status
        self.save('is_active')
    
    def add_child(self, child):
        self.children[child.username] = child
        
    def change_info(self, desc, flags, can_weblogin, can_post, need_check):
        self.description = desc
        self.flags = flags
        if can_weblogin:
            self.can_weblogin = 1
        else:
            self.can_weblogin = 0
      
        if can_post:
            self.can_post = 1
        else:
            self.can_post = 0      

        if need_check:
            self.need_check = 1
        else:
            self.need_check = 0

        self.save('description,flags,can_weblogin,can_post,need_check')
    
    def change_cm(self, cm):
        if self.channel_cm != cm:
            self.channel_cm = cm
            self.save('channel_cm')
           
    def change_cu(self, cu):
        if self.channel_cu != cu:
            self.channel_cu = cu
            self.save('channel_cu')
    
    def change_ct(self, ct):
        if self.channel_ct != ct:
            self.channel_ct = ct
            self.save('channel_ct')
    
    def change_cm_r(self, cm):
        self.change_cm(cm)
        for u in self.children.itervalues():
            u.change_cm_r(cm)
    
    def change_cu_r(self, cu):
        self.change_cu(cu)
        for u in self.children.itervalues():
            u.change_cu_r(cu)
    
    def change_ct_r(self, ct):
        self.change_ct(ct)
        for u in self.children.itervalues():
            u.change_ct_r(ct)
    
    def set_ext(self,ext):
        self.ext = ext
        self.save('ext')
    
    def set_msg_postfix(self, msg_postfix):
        try:
            sql = '''
            update user set msg_postfix = '%s' where uid = '%d'
            ''' % (msg_postfix, self.uid)
            self.db.raw_sql_query(sql)
        except:
            print_exc()
            return 1
        return 0
    
    def set_all_child_msg_postfix(self, msg_postfix):
        try:
            self.set_msg_postfix(msg_postfix)
            for key, u in self.children.iteritems():
                ret = u.set_all_child_msg_postfix(msg_postfix)
                if ret == 1:
                    return ret
        except:
            print_exc()
            return 1
        return 0
    def is_admin(self):
        return self.flags == user.F_CHARGE | user.F_CREATE_CHARGE | user.F_CREATE_USER
    
    def is_user(self):
        return self.flags == 0
    
    def is_agent(self):
        return self.flags == user.F_CHARGE | user.F_CREATE_USER
    
    def delete_child(self, child):
        del self.children[child.username]
        child.delete_allchildren()
        before_num = self.msg_num
        self.add_message(child.msg_num)
        try:
            self.db.raw_sql('INSERT INTO addmsglog(username,before_msg_num,add_msg_num,after_msg_num,type,create_time) VALUES(%s,%s,%s,%s,%s,%s)',
                (self.username, before_num, child.msg_num, self.msg_num, 1, datetime.now()))
        except:
            pass
        child.delete()

    def delete_allchildren(self):
        for c in self.children:
            c.delete_allchildren()
            c.delete()
        self.children = {}
    def to_json(self):
        d = {}
        d['uid'] = self.uid
        d['parent_id'] = self.parent_id
        d['username'] = self.username
        d['description'] = self.description
        d['msg_num'] = self.msg_num
        d['flags'] = self.flags
        d['is_active'] = self.is_active
        d['create_time'] = self.create_time.strftime("%y-%m-%d %H:%M")
        d['is_can_weblogin'] = self.can_weblogin
        d['is_can_post'] = self.can_post
        d['is_need_check'] = self.need_check
        d['cm'] = self.channel_cm
        d['cu'] = self.channel_cu
        d['ct'] = self.channel_ct
        d['commit_num'] = self.commit_num
        d['ext'] = self.ext
        d['percent'] = self.percent
        d['msg_postfix'] = self.msg_postfix
        if self.last_login == None:
            d['last_login'] = None
        else:
            d['last_login'] = self.last_login.strftime("%y-%m-%d %H:%M")
        # d['commit_times'] = len(self.commits)
        return d
    
    def to_json_all(self):
        d = self.to_json()
        
        l = []
        for i in self.children.itervalues():
            l.append(i.to_json_all())
        d['children'] = l
        # d['commit_times'] = len(self.commits)
        return d
