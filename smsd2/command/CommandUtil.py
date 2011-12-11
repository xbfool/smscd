'''
Created on 2011-10-6

@author: xbfool
'''

def ret_util(ret, errno=-1, errmsg='command exec failed'):
    if ret or ret is []:
        return {'errno': 0, 'errtext':'command exec success', 'ret': ret}
    else:
        return {'errno': errno, 'errtext':errmsg, 'ret': ret}  
