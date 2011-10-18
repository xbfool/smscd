'''
Created on 2011-10-18

@author: xbfool
'''
from xml.dom.minidom import parseString
import db_controller
from traceback import print_exc

def process_ret_hlyd(sender, param):
    result = 'message send fail'
    try:
        resultDOM = parseString(param['ret'][2])
        result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.data
    
        if result == '0':
            db_controller.send_success(sender.__db, param, result)
        else:
            db_controller.send_fail(sender.__db, param, result)
        
    except:
        print_exc()
        db_controller.send_fail(sender.__db, param, result)
  
    return 1

