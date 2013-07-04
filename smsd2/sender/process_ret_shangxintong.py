'''
Created on 2011-10-18

@author: xbfool
'''

from xml.dom.minidom import parseString

from traceback import print_exc
def process_ret_shangxintong(sender, param):
    success_str = '<Result>1</Result>'
    result = "something is error"
    try:
        resultDOM = parseString(param['ret'][2])
        result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.nextSibling.firstChild.data

        
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

def process_ret_qixintong2012(sender, param):
    result = "something is error"
    try:
        resultDOM = parseString(param['ret'][2])
        result = resultDOM.firstChild.firstChild.firstChild.data

        if result == '1':
            sender.msg_controller.send_success(param, result)
            return 1
        elif result in ('0', '-2', '-3', '-20', '1007', '-1007', '-99', '99'):
            return -2
        elif result in ('-1', '-10', '-11', '-17', '-18', '-19', '-99'):
            return -2
        else:
            return -2
            
    except:
        import string
        success_str = '<Result>1</Result>'
        if string.find(param['ret'][2], success_str):
            sender.msg_controller.send_success(param, result)
            return 1
            
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2
    
    return 1

def process_ret_106f(sender, param):
    result = "something is error"
    try:
        resultDOM = parseString(param['ret'][2])
        result = resultDOM.firstChild.firstChild.firstChild.data

        if result in ('00', '01', '03'):
            sender.msg_controller.send_success(param, result)
            return 1
        elif result in ('06', '07', '08', '09', '10', '97', '98', '99'):
            return -2
        elif result in ('02', '04', '05'):
            return -1
        else:
            return -2

    except:
        import string
        success_str = '<code>03</code>'
        if string.find(param['ret'][2], success_str):
            sender.msg_controller.send_success(param, result)
            return 1
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2

    return 1

