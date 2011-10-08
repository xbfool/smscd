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
        
    def add(self, **args):
        try:
            ins = self.table.insert().values(**args)
            self.c.db.execute(ins)
            return True
        except:
            return False
    
    def delete(self, uid):
        try:
            d = self.table.delete(self.table.c.uid==uid)
            self.c.db.execute(d)
            return True
        except:
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
            ret = dict(r.items())
            return ret
        except:
            print_exc()
            return None
        
    def query_all(self):
        sel = select([self.table])
        res = self.c.db.execute(sel)
        rlist = []
        for r in res:
            rlist.append(dict(r.items()))
        return rlist
    
    
class ChannelListController(object):
    def __init__(self, context):
        self.c = context
        self.table = Table('ChannelList', self.c.meta, autoload=True, autoload_with=self.c.db)
    
    def add(self, **args):
        try:
            ins = self.table.insert().values(**args)
            self.c.db.execute(ins)
            return True
        except:
            return False
    
    def delete(self, uid):
        try:
            d = self.table.delete(self.table.c.uid==uid)
            self.c.db.execute(d)
            return True
        except:
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
            ret = dict(r.items())
            return ret
        except:
            print_exc()
            return None
        
    def query_all(self):
        sel = select([self.table])
        res = self.c.db.execute(sel)
        rlist = []
        for r in res:
            rlist.append(dict(r.items()))
        return rlist
