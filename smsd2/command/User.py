'''
Created on 2011-10-6

@author: xbfool
'''

from sqlalchemy import Table, select
from smsd2.command.session import get_session_id, check_session_id, update_session_id
from traceback import print_exc

class UserController(object):
    def __init__(self, context):
        self.c = context
        self.user_t = Table('user', self.c.meta, autoload=True, autoload_with=self.c.db)
        self.session_t =  Table('sessions', self.c.meta, autoload=True, autoload_with=self.c.db)
        self.channel_list_t = Table('ChannelList', self.c.meta, autoload=True, autoload_with=self.c.db)
        
    def login(self, username, password):
        try:
            sel = select([self.user_t], self.user_t.c.username==username)
            res = self.c.db.execute(sel)
            user = res.fetchone()
            u = dict(user.items())

            if user.password == password:
                sid = get_session_id(username, password)
                update_session_id(self.c, user.uid, sid)
                print user
                return {'user':u, 'sid':sid}
            else:
                return None
        except:
            print_exc()
            return None  
        
    def __channel_list_exist(self, id):
        try:
            sel = select([self.channel_list_t], self.channel_list_t.c.uid==id)
            res = self.c.db.execute(sel)
            r =  res.fetchone()
            if r:
                return True
            else:
                return False
        except:
            print_exc()
            return False
        
    def query_all(self):
        sel = select([self.user_t])
        res = self.c.db.execute(sel)
        rlist = []
        if res != None:
            for r in res:
                rlist.append(dict(r.items()))
        return rlist
    
    def update_channel_list(self, uid, channel_list_id, cm, cu, ct):
        #chanel_list_id == -1 for use none of the id's
        try:
            if not self.__channel_list_exist(channel_list_id) and channel_list_id != -1:
                return False
   
            up = self.user_t.update().where(self.user_t.c.uid == uid).values(\
            channel_list_id = channel_list_id,
            channel_cm = cm,
            channel_cu = cu,
            channel_ct = ct)
            
            self.c.db.execute(up)
            return True
        except:
            print_exc()
            return False