'''
Created on 2011-10-18

@author: xbfool
'''

from traceback import print_exc
def process_ret_scp_0591(sender, param):
    result = 'message send fail'
    rl = []
    try:
        result = param['ret'][2]
        rl = result.split(';')
        if rl[0] == 'ResultCode=0':
            sender.msg_controller.send_success(param, result)
            return 1
        else:
            return -1
      
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return 0
  
    return 1