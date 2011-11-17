'''
Created on 2011-10-18

@author: xbfool
'''

from xml.dom.minidom import parseString

from traceback import print_exc
def process_ret_hb_ct(sender, param):
    result = 'message send fail'
    try:
        resultDOM = parseString(param['ret'][2])
        result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.data
        
        if result == 'messageSuccess':
            sender.msg_controller.send_success(param, result)
            return 1
        elif result == 'illegal keywords':
            return -1
        elif result == 'not enugh money!':
            return -1
        else:
            return -1
#        
    except:
        print_exc()
        return -1
  
    return 1  

