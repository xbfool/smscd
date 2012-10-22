'''
Created on 2012-3-13

@author: xbfool
'''
'''
Created on 2011-10-19

@author: xbfool
'''
from smsd2.database.db_engine import create_db
from smsd2.config.config_reader import loadcfg
from sqlalchemy import Table, select
from msg_status import msg_status, channel_status
from sqlalchemy import MetaData
from settings import sender_settings
import phonenumber
import time
from datetime import datetime
from traceback import print_exc
from sqlalchemy.sql import and_, or_, not_
import msg_util
from random import seed, shuffle,random
def dump(path, username):
    ph = phonenumber.phonenumber()
    ct = open(path+username+'_address.csv', 'w')
    f = ct
    c = msg_util.MsgController()
    sel =  select([c.msg_t], and_(#c.msg_t.c.status == 2, \
                                  c.msg_t.c.user_uid == c.user_t.c.uid,\
                                  #c.msg_t.c.channel == 'honglian_jtyh',\
                                  c.user_t.c.username == username,\
                                  #c.msg_t.c.create_time >= '20120908'
                                  ))

    res = c.db.execute(sel)
    addr_set = set()
    for i in res:
        addr = i.address.split(';')
        #print addr
        addr_set = addr_set.union(addr)
      
    print len(addr_set) 
    for j in addr_set:
        t = '%s\r\n' % (j)
        f.write(t)
                                             
if __name__ == '__main__':
    dump('/tmp/', 't80028')
