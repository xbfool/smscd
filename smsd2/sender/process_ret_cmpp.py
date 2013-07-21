__author__ = 'xbfool'
import urllib

from traceback import print_exc
def process_ret_cmpp_web(sender, param):
    result = 'message send fail'

    try:
        result = param['ret'][2]
        rl = result.split('|')
        if rl[0] == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        else:
            return -2
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2
    return -2