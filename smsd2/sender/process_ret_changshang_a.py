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
        elif result == u'100' or result == u'101' or result == 100 or result == 101:
            return -1 #channel error
        elif result == u'102' or result == u'103' or result == 102 or result == 103:
            return -2 #msg_error
        elif result == u'109' or result == '109' or result == 109:
            return -1
        else:
            return -1
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return 0
        
    return 1  
