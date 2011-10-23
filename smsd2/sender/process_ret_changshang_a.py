'''
Created on 2011-10-18

@author: xbfool
'''

from traceback import print_exc

def process_ret_changshang_a(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2] 
        if result[0] == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        else:
            return 0
        
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return 0
        
    return 1  