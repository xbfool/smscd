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
    t = '%s,%s,%s,%s,%s\r\n' % ('send_time','address','channel','status','message')
    ct = open(path+'ct.csv', 'w')
    ct.write(t)
    cu = open(path+'cu.csv', 'w')
    cu.write(t)
    cm = open(path+'cm.csv', 'w')
    cm.write(t)
    f = cm
    c = msg_util.MsgController()
    sel =  select([c.msg_t, c.channel_item_t.c.desc, c.user_t.c.percent], and_(c.msg_t.c.status == msg_status.F_SEND, \
                                  c.msg_t.c.user_uid == c.user_t.c.uid,\
                                  c.user_t.c.username == username,\
                                  c.channel_item_t.c.name == c.msg_t.c.channel,\
                                  ))

    res = c.db.execute(sel)
    for i in res:
        addr = i.address.split(';')
        #print addr
        channel = ph.check_addr(addr[0])
        if channel == ph.S_CM:
            f = cm
        elif channel == ph.S_CU:
            f = cu
        elif channel == ph.S_CT:
            f = ct
        l = len(addr) * i.sub_num / i.msg_num

        my_seed = i.seed
	if my_seed == None:
            continue
        ret1 = []
        ret2 = []
        
        addr.sort()
        seed(my_seed)
        shuffle(addr)
            
        ret1 = addr[0:l]
        ret2 = addr[l:]
        for addr_s in ret1:	
            t1 = '%s,%s,%s,%d,%s\r\n' % (\
                                             i.last_update,\
                                             addr_s,\
                                             i.desc,\
                                             0,\
                                             i.msg.decode('utf8').encode('gbk'))
            f.write(t1)
        
        seed(i.uid + len(i.msg) * my_seed + len(addr))
        for addr_s in ret2:
            s = 'null'
             
            if random() < 0.25:
                s = '1'
            t2 = '%s,%s,%s,%s,%s\r\n' % (\
                                             i.last_update,\
                                             addr_s,\
                                             i.desc,\
                                             s,\
                                             i.msg.decode('utf8').encode('gbk'))
            f.write(t2)            
                                             
if __name__ == '__main__':
    dump('/tmp/', '10053')
