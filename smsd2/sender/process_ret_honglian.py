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
        print param
        sender.msg_controller.send_success(param, result)
        return 1
    elif param['ret'][2] == 'error:\xd3\xe0\xb6\xee\xb2\xbb\xd7\xe30': #no money
        return -1
    elif result in ('001', '010', '100', '101', '110', '011', '111'):
        return -2
    else:
        return 0
        
    return 1
