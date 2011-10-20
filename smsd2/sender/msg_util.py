'''
Created on 2011-10-19

@author: xbfool
'''
from smsd2.database.db_engine import create_db
from smsd2.config.config_reader import loadcfg
from sqlalchemy import Table, select
from msg_status import *
from sqlalchemy import MetaData
from settings import sender_settings
import phonenumber
import time
class msg_send():
    def __init__(self):
        self.addr = []
        self.content = ""
        self.channel = ""
        self.user_uid = 0
        self.uid = 0
        self.msg_num = 0
        self.percent = 0
        self.ext = ""
        
class channel_list():
    pass
class MsgController():
    def __init__(self):
        self.cfg = loadcfg('config.yaml')
        self.db = create_db(self.cfg)
        self.meta = MetaData()
        self.msg_t = Table('message', self.meta, autoload=True, autoload_with=self.db)
        self.user_t = Table('user', self.meta, autoload=True, autoload_with=self.db)
        self.channel_list_t = Table('channellist', self.meta, autoload=True, autoload_with=self.db)
        self.channel_item_t = Table('channelitem', self.meta, autoload=True, autoload_with=self.db)
        self.channel_list_dict = {}
        self.channel_item_dict = {}
        self.channel_item_name_dict = {}
        self.user_dict = {}
        self.settings = sender_settings().settings
        self.default_list = None
        
    def clean_dict(self):
        self.user_dict = {}
        self.channel_list_dict = {}
        self.channel_item_dict = {}
        self.channel_item_name_dict = {}
        self.settings = sender_settings().settings
        self.default_list = None
        
    def get_messages(self):
        sel =  select([self.msg_t], self.msg_t.c.status == msg_status.F_ADMIT)
        res = self.db.execute(sel)
        
        for r in res:
            ret = dict(r.items())
            ret['content'] = ret['msg']
            ret['percent'] = self.get_user_percent(ret['user_uid'])
            yield ret
            time.sleep(10)
    def get_user_percent(self, user_uid):
        if self.user_dict.get(user_uid):
            return self.user_dict[user_uid].percent
        
        sel = select([self.user_t], self.user_t.c.uid == user_uid)
        res = self.db.execute(sel)
        r = res.fetchone()
        if r != None:
            self.user_dict[user_uid] = r
            return r.percent
        else:
            return 100
    def get_channel_list(self, msg):
        channel_list_id = self._get_user_channel_list_id(msg)
        l = self._get_user_channel_list(channel_list_id)
        if not l:
            l = self._get_old_channel_list(msg['user_uid'])
        
        try:
            pm = phonenumber.phonenumber()
            channel_type = pm.check_addr(msg['addr'][0])
            if channel_type == pm.S_CM:
                return l.cm
            elif channel_type == pm.S_CU:
                return l.cu
            elif channel_type == pm.S_CT:
                return l.ct
        except:
            return l.cu
        
    
    def _get_user_channel_list_id(self, msg):
        sel = select([self.user_t], self.user_t.c.uid == msg['user_uid'])
        res = self.db.execute(sel)
        r = res.fetchone()
        if r != None:
            return r.channel_list_id
        else:
            return -1
        
    def _get_user_channel_list(self, channel_list_id):
        sel = select([self.channel_list_t], self.channel_list_t.c.uid == channel_list_id)
        res = self.db.execute(sel)
        r = res.fetchone()
        c = channel_list() 
        if r == None:
            return None
        if self.channel_list_dict.get(channel_list_id):
            return self.channel_list_dict.get(channel_list_id)
        c.name = r.name
        c.desc = r.desc
        c.cm = []
        c.cu = []
        c.ct = []
        for i in (r.cm1, r.cm2, r.cm3):
            c.cm.append(self._get_user_channel_item(i))
        for i in (r.cu1, r.cu2, r.cu3):
            c.cu.append(self._get_user_channel_item(i))
        for i in (r.ct1, r.ct2, r.ct3):
            c.ct.append(self._get_user_channel_item(i))
        
        self.channel_list_dict[channel_list_id] = c
        default = self._get_default_channel_list()
        if default:
            c.cm.extend(default.cm)
            c.cu.extend(default.cu)
            c.ct.extend(default.ct)
        return c
    
    def _get_default_channel_list(self):
        if self.default_list:
            return self.default_list
        sel = select([self.channel_list_t], self.channel_list_t.c.name == 'default')
        res = self.db.execute(sel)
        r = res.fetchone()
        c = channel_list() 
        if r == None:
            return None

        c.name = r.name
        c.desc = r.desc
        c.cm = []
        c.cu = []
        c.ct = []
        for i in (r.cm1, r.cm2, r.cm3):
            c.cm.append(self._get_user_channel_item(i))
        for i in (r.cu1, r.cu2, r.cu3):
            c.cu.append(self._get_user_channel_item(i))
        for i in (r.ct1, r.ct2, r.ct3):
            c.ct.append(self._get_user_channel_item(i))
        
        self.default_list = c
        return c
    
    def _get_old_channel_list(self, user_uid):
        sel = select([self.user_t], self.user_t.c.uid == user_uid)
        res = self.db.execute(sel)
        r = res.fetchone()
        c = channel_list() 
        c.name = 'old_list'
        c.desc = 'old_list'
        print r.channel_cm,r.channel_cu, r.channel_ct
        c.cm = [self._get_channe_item_by_name(r.channel_cm)]
        c.cu = [self._get_channe_item_by_name(r.channel_cu)]
        c.ct = [self._get_channe_item_by_name(r.channel_ct)]
        default = self._get_default_channel_list()
        if default:
            c.cm.extend(default.cm)
            c.cu.extend(default.cu)
            c.ct.extend(default.ct)
        
        return c
    def _get_channe_item_by_name(self, name):
        if self.channel_item_name_dict.get(name):
            return self.channel_item_name_dict.get(name)
        sel = select([self.channel_item_t], self.channel_item_t.c.name == name)
        res = self.db.execute(sel)
        r = res.fetchone()
        r_d = dict(r.items())
        self.channel_item_name_dict[name] = r_d
        r_d['setting'] = self.settings.get(name)
        return r_d
        
    def _get_user_channel_item(self, item_id):
        
        if self.channel_item_dict.get(item_id):
            return self.channel_item_dict.get(item_id)
        
        sel = select([self.channel_item_t], self.channel_item_t.c.uid == item_id)
        res = self.db.execute(sel)
        r = res.fetchone()
        r_d = dict(r.items())
        self.channel_item_dict[item_id] = r_d
        r_d['setting'] = self.settings.get(r.name)
        return r_d
        
    def _print_channel_item(self, channel_name, item):
        print channel_name, " item name: %s, desc: %s, status: %s, last_update: %s, setting: %s" %\
            (item['name'], item['desc'], item['status'], item['last_update'], item['setting'])
            
    def _print_channel_list(self, list):
        print "list name: %s, desc %s" % (list.name, list.desc)
        for i in range(len(list.cm)):
            self._print_channel_item('cm'+str(i+1), list.cm[i])
        for i in range(len(list.cu)):
            self._print_channel_item('cu'+str(i+1), list.cu[i])
        for i in range(len(list.ct)):
            self._print_channel_item('ct'+str(i+1), list.ct[i])   
            

