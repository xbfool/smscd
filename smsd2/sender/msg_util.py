'''
Created on 2011-10-19

@author: xbfool
'''
from smsd2.database.db_engine import create_db
from smsd2.config.config_reader import loadcfg
from sqlalchemy import Table, select
from msg_status import *
from sqlalchemy import MetaData
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
class MsgController():
    def __init__(self):
        self.cfg = loadcfg('config.yaml')
        self.db = create_db(self.cfg)
        self.meta = MetaData()
        self.msg_t = Table('message', self.meta, autoload=True, autoload_with=self.db)
        self.user_t = Table('user', self.meta, autoload=True, autoload_with=self.db)
        
    def get_messages(self):
        sel =  select([self.msg_t], self.msg_t.c.status == msg_status.F_ADMIT)
        res = self.db.execute(sel)
        
        for r in res:
            ret = dict(r.items())
            yield ret
            time.sleep(10)
            

def get_processor(msg):
    pass