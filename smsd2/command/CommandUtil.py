'''
Created on 2011-10-6

@author: xbfool
'''

def ret_util(ret):
    if ret or ret is []:
        return {'errno': 0, 'errtext':'command exec success', 'ret': ret}
    else:
        return {'errno': -1, 'errtext':'command exec failed', 'ret': ret}  
