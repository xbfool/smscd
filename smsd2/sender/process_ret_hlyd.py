'''
Created on 2011-10-18

@author: xbfool
'''
from xml.dom.minidom import parseString

from traceback import print_exc

def process_ret_hlyd(sender, param):
    result = 'message send fail'
    try:
        resultDOM = parseString(param['ret'][2])
        result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.data
    
        if result == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        else:
            return 0
        
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return 0
  
    return 1

