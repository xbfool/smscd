# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-4

@author: xbfool
'''
from sqlalchemy import Table, select

from traceback import print_exc
from datetime import datetime
class ChannelItem(object):
    def __init__(self, uid, name, desc, type):
        self.uid = uid
        self.name = name
        self.desc = desc
        self.type = type
    
class ChannelItemController(object):
    def __init__(self, context):
        self.c = context
        self.table = Table('ChannelItem', self.c.meta, autoload=True, autoload_with=self.c.db)
        self.channel_list_t = Table('ChannelList', self.c.meta, autoload=True, autoload_with=self.c.db)
    def add(self, **args):
        try:
            ins = self.table.insert().values(**args)
            self.c.db.execute(ins)
            return True
        except:
            return False
    
    def delete(self, uid):
        try:
            if self.__channel_item_used(uid):
                return False
            d = self.table.delete(self.table.c.uid==uid)
            self.c.db.execute(d)
            return True
        except:
            return False
    
    def __channel_item_used(self, id):
        try:
            sel = select([self.channel_list_t], self.channel_list_t.c.cm1==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.cm2==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.cm3==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.cu1==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.cu2==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.cu3==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.ct1==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.ct2==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            sel = select([self.channel_list_t], self.channel_list_t.c.ct3==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            
            return False
        except:
            print_exc()
            return False
    def update(self, uid, **args):
        try:
            up = self.table.update().where(self.table.c.uid == uid).values(**args)
            self.c.db.execute(up)
            up = self.table.update().\
                where(self.table.c.uid == uid).\
                values(last_update=datetime.now())
            self.c.db.execute(up)
            return True
        except:
            print_exc()
            return False
    
    def query_by_name(self, nameArg):
        try:
            sel = select([self.table], self.table.c.name==nameArg)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            ret = {}
            if r:
                ret = dict(r.items())
            return ret
        except:
            print_exc()
            return None
    
    def query_by_uid(self, uid):
        try:
            sel = select([self.table], self.table.c.uid==uid)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            ret = {}
            if r:
                ret = dict(r.items())
            return ret
        except:
            print_exc()
            return None
        
    def query_all(self):
        sel = select([self.table])
        res = self.c.db.execute(sel)
        rlist = []
        if res != None:
            for r in res:
                rlist.append(dict(r.items()))
        return rlist
    
    
class ChannelListController(object):
    def __init__(self, context):
        self.c = context
        self.table = Table('ChannelList', self.c.meta, autoload=True, autoload_with=self.c.db)
        self.user_t = Table('user', self.c.meta, autoload=True, autoload_with=self.c.db)
    def add(self, **args):
        try:
            ins = self.table.insert().values(**args)
            self.c.db.execute(ins)
            return True
        except:
            return False
    
    def delete(self, uid):
        try:
            if self.__channel_list_used(uid):
                return False
            d = self.table.delete(self.table.c.uid==uid)
            self.c.db.execute(d)
            return True
        except:
            return False
    
    def __channel_list_used(self, id):
        try:
            sel = select([self.user_t], self.user_t.c.channel_list_id==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            else:
                return False
        except:
            print_exc()
            return False
    def update(self, uid, **args):
        try:
            up = self.table.update().where(self.table.c.uid == uid).values(**args)
            self.c.db.execute(up)
            return True
        except:
            print_exc()
            return False
    
    def query_by_name(self, nameArg):
        try:
            sel = select([self.table], self.table.c.name==nameArg)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            ret = {}
            if r:
                ret = dict(r.items())
            return ret
        except:
            print_exc()
            return None
    
    def query_by_uid(self, uid):
        try:
            sel = select([self.table], self.table.c.uid==uid)
            res = self.c.db.execute(sel)
            ret = {}
            r =  res.fetchone()
            if r:
                ret = dict(r.items())
            return ret
        except:
            print_exc()
            return None
        
    def query_all(self):
        sel = select([self.table])
        res = self.c.db.execute(sel)
        rlist = []
        if res != None:
            for r in res:
                rlist.append(dict(r.items()))
        return rlist
