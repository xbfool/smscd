# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from traceback import print_exc
def process_ret_zhangshangtong(sender, param):
    result = 'message send fail'
    rl = []
    msg_err = ('3016', '3017', '3018', '4004', '3011', '3013',
    	'3042', '3012', '3000', '3003', '3032', '3021')
    channel_err = ('1006', '1003', '1008', '1004', '1007', '3014', '3091')
    try:
        result = param['ret'][2]
        rl = result.split('|')
        if rl[0] == '1':
            sender.msg_controller.send_success(param, result)
            return 1
        elif rl[0] in msg_err:
            return -2
        elif rl[0] in channel_err:
            return -1
        else:
            return -1
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return 1
  
    return 1