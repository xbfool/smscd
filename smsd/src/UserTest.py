'''
Created on 2011-10-3

@author: Administrator
'''

from Utility import *
from UserN import UserN

if __name__ == '__main__':
    session = Session()
    userlist = session.query(UserN).all()
    for user in userlist:
        print user.username
    user = UserN("test", "test", "123", "179", 1000, 1, 1, 1, '', '', '', 0, 100)
    session.add(user)
    userlist = session.query(UserN).all()
    i = 0
    for user in userlist:
        print user.username
        print 'before'
        for key,val in user.test.items():
            print str(val)
        user.test[i] = i
        print 'after'
        for key,val in user.test.items():
            print str(val)
        i = i+1