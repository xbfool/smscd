'''
Created on 2011-10-18

@author: xbfool
'''
import urllib

from traceback import print_exc

def process_ret_honglian(sender, param):
    success_str = "00"
    try:
        resultstr = param['ret'][2]
        result = urllib.unquote(resultstr)
        result = result.decode('gbk').encode('utf8')
    except:
        print_exc()
        result = "something is error"
        
    if result == success_str:
        sender.msg_controller.send_success(param, result)
    else:
        sender.msg_controller.send_fail(param, result)
        
    return 1
