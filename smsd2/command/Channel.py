# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-4

@author: xbfool
'''
from sqlalchemy import Table, Column, Integer, String, select, DefaultClause
from sqlalchemy.types import DateTime
from traceback import print_exc
from datetime import datetime
class ChannelItem(object):
    def __init__(self, uid, name, desc, type):
        self.uid = uid
        self.name = name
        self.desc = desc
        self.type = type
    
def CreateChannelItemTable(meta, db):
        channel = Table('ChannelItem', meta,
            Column('uid', Integer, primary_key = True),
            Column('name', String(50), nullable = False, unique = True),
            Column('desc', String(50)),
            Column('type', String(50), nullable = False),
            Column('status', Integer, DefaultClause("0")),
            Column('last_update', DateTime)
            )
        meta.create_all(tables=[channel],bind=db)
    
def CreateChannelListTable(meta, db):
        list = Table('ChannelList', meta,
            Column('uid', Integer, primary_key = True),
            Column('name', String(50), nullable = False, unique = True),
            Column('desc', String(100)),
            Column('cm1', Integer, DefaultClause("-1")),
            Column('cm2', Integer, DefaultClause("-1")),
            Column('cm3', Integer, DefaultClause("-1")),
            Column('cu1', Integer, DefaultClause("-1")),
            Column('cu2', Integer, DefaultClause("-1")),
            Column('cu3', Integer, DefaultClause("-1")),
            Column('ct1', Integer, DefaultClause("-1")),
            Column('ct2', Integer, DefaultClause("-1")),
            Column('ct3', Integer, DefaultClause("-1")),
            )
        meta.create_all(tables=[list],bind=db)
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
            return res.fetchone()
        except:
            print_exc()
            return None
    
    def query_by_uid(self, uid):
        try:
            sel = select([self.table], self.table.c.uid==uid)
            res = self.c.db.execute(sel)
            return res.fetchone()
        except:
            print_exc()
            return None
        
    def query_all(self):
        sel = select([self.table])
        res = self.c.db.execute(sel)
        ret = res.fetchall()
        return ret
    
    
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
            return res.fetchone()
        except:
            print_exc()
            return None
    
    def query_by_uid(self, uid):
        try:
            sel = select([self.table], self.table.c.uid==uid)
            res = self.c.db.execute(sel)
            return res.fetchone()
        except:
            print_exc()
            return None
        
    def query_all(self):
        sel = select([self.table])
        res = self.c.db.execute(sel)
        ret = res.fetchall()
        return ret
