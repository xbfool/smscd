'''
Created on 2011-10-6

@author: xbfool
'''

from hashlib import sha1
from datetime import datetime
def get_session_id(username, password):
    sid = sha1(username)
    sid.update(password)
    sid.update(str(datetime.now()))
    return sid.hexdigest()

def check_session_id(context, sid):
    pass

def update_session_id(context, user_uid, sid):
    pass