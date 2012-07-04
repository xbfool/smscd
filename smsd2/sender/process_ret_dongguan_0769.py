'''
Created on 2011-10-18

@author: xbfool
'''
from traceback import print_exc


def process_ret_dongguan_0769(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2]         
        if result[0] == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        else:
            return -2
        
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2
  
    return 1  