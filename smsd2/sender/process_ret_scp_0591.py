'''
Created on 2011-10-18

@author: xbfool
'''

import db_controller
from traceback import print_exc
def process_ret_scp_0591(sender, param):
    result = 'message send fail'
    rl = []
    try:
        result = param['ret'][2]
        print result
        rl = result.split(';')

        if rl[0].split('=')[1] == '0':
            db_controller.send_success(sender.__db, param, result)
        else:
            if len(rl) == 2:
                try:
                    result = rl[1].split('=')[1].decode('gbk').encode('utf8')
                except:
                    pass
            db_controller.send_fail(sender.__db, param, result)
        
    except:
        print_exc()
        db_controller.send_fail(sender.__db, param, result)
  
    return 1