'''
Created on 2011-10-18

@author: xbfool

'''
import urllib
import db_controller
from traceback import print_exc
def process_ret_sd_ct(sender, param):
    result = "something is error"
    success_str = "Information%3a%e6%b6%88%e6%81%af%e5%8f%91%e9%80%81%e6%88%90%e5%8a%9f%ef%bc%8c%e8%af%b7%e6%9f%a5%e7%9c%8b%e4%ba%92%e5%8a%a8%e4%bf%a1%e7%ae%b1%ef%bc%81%09"
    try:
        resultstr = param['ret'][2]
        result = urllib.unquote(resultstr)
    except:
        pass
    try:
        if resultstr == success_str:
            db_controller.send_success(sender.__db, param, result)
        else:
            db_controller.send_fail(sender.__db, param, result)
            
    except:
        print_exc()
        db_controller.send_fail(sender.__db, param, result)
  
    return 1

