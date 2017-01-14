'''
Created on 2011-10-1
8
@author: xbfool
'''
from xml.dom.minidom import parseString

from traceback import print_exc

def process_ret_hlyd(sender, param):
    result = "something is error"
    try:
        result = param['ret'][2]
        rl = result.split(':')

        if rl[0] == 'ok':
            sender.msg_controller.send_success(param, result)
            return 1
        elif rl[0] == 'error':
            return -2
        elif rl[0] == 'fail':
            return -2
        else:
            return -2
            
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2
    
    return -2

