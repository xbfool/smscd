'''
Created on 2011-10-18

@author: xbfool
'''


import db_controller
from traceback import print_exc

def process_ret_maoming_ct(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2]
        if result == '0\r\n':
            db_controller.send_success(sender.__db, param, result)
        else:
            db_controller.send_fail(sender.__db, param, result)
        
    except:
        print_exc()
        db_controller.send_fail(sender.__db, param, result)
  
    return 1
