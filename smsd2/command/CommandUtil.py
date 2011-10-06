'''
Created on 2011-10-6

@author: xbfool
'''

def ret_util(ret):
    if ret:
        return {'errno': 0, 'errtext':'command exec success', 'value': ret}
    else:
        return {'errno': -1, 'errtext':'command exec failed', 'value': ret}  
