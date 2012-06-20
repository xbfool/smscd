'''
Created on 2011-10-18

@author: xbfool

'''
import urllib

from traceback import print_exc
def process_ret_sd_ct(sender, param):
    result = "something is error"
    success_str = "Information%3a%e6%b6%88%e6%81%af%e5%8f%91%e9%80%81%e6%88%90%e5%8a%9f%ef%bc%8c%e8%af%b7%e6%9f%a5%e7%9c%8b%e4%ba%92%e5%8a%a8%e4%bf%a1%e7%ae%b1%ef%bc%81%09"
    channel_error_str = "Information%3a%e5%b8%90%e5%8f%b7%e4%bd%99%e9%a2%9d%e4%b8%8d%e8%b6%b3%ef%bc%81"
    try:
        resultstr = param['ret'][2]
        result = urllib.unquote(resultstr)
    except:
        pass
    try:
        if resultstr == success_str:
            sender.msg_controller.send_success(param, result)
            return 1
        elif resultstr == channel_error_str:
            return -1
        else:
            return -1
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -1
  
    return 1

