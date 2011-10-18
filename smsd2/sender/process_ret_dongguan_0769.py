'''
Created on 2011-10-18

@author: xbfool
'''
from traceback import print_exc
import db_controller

def process_ret_dongguan_0769(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2]         
        if result[0] == '0':
            db_controller.send_success(sender.__db, param, result)
        else:
            db_controller.send_fail(sender.__db, param, result)
        
    except:
        print_exc()
        db_controller.send_fail(sender.__db, param, result)
  
    return 1  