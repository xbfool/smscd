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

def process_ret_hb_ct_2(sender, param):
    result = 'message send fail'
    try:
        resultDOM = parseString(param['ret'][2])
        result1 = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild
        ret1_text = result1.firstChild.data
        result2 = result1.nextSibling
        ret2_text = result2.firstChild.data
        result3 = result2.nextSibling
        ret3_text = result3.firstChild.data
        ret = ret2_text.split('-')
        result = '.'.join((ret1_text, ret2_text, ret3_text))
        if ret[0] == 'SUCC':
            sender.msg_controller.send_success(param, result)
            return 1
        else if ret[0] == 'FAIL':
            if ret[1] == '200':
                sender.msg_controller.send_result(param, result)
                return -1
        if ret[1] == '300':
            sender.msg_controller.send_result(param, result)
            return -1
        
        sender.msg_controller.send_fail(param, result)
        return 0
    except:
        sender.msg_controller.send_fail(param, result)
        return 0

    return 1