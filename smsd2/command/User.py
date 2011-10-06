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