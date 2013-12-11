'''
Created on 2011-10-18

@author: xbfool
'''

from traceback import print_exc
from xml.dom.minidom import parseString

def process_ret_changshang_a(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2] 
        if result[0] == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        elif result == u'100' or result == u'101' or result == 100 or result == 101:
            return -1 #channel error
        elif result == u'102' or result == u'103' or result == 102 or result == 103:
            return -2 #msg_error
        elif result == u'109' or result == '109' or result == 109:
            return -1
        else:
            return -1
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2
        
    return 1  

def process_ret_106g(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2]
        if result[0] == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        elif result == '-1' or result == -1:
            return -1
        elif result == '-2' or result == -2:
            return -1
        elif result == '-3' or result == -3:
            return -2
        elif result == '-4' or result == -4:
            return -2
        elif result == '-5' or result == -5:
            return -2
        elif result == '-6' or result == -6:
            return -1
        else:
            return -2
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2

    return 1

def process_ret_106h(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2]
        x = parseString(result)
        result = int(x.firstChild.firstChild.data)

        if result == '0' or result == 0:
            sender.msg_controller.send_success(param, result)
            return 1
        elif result == '-1' or result == -1:
            return -1
        elif result == '-2' or result == -2:
            return -1
        elif result == '-3' or result == -3:
            return -1
        elif result == '-4' or result == -4:
            return -2
        elif result == '-5' or result == -5:
            return -2
        elif result == '-6' or result == -6:
            return -2
        elif result[1] == '7':#-7
            return -2
        elif result == '-8' or result == -8:
            return -1
        elif result == '-9' or result == -9:
            return -1
        elif result == '-10' or result == -10:
            return -2
        elif result == '-11' or result == -11:
            return -2
        elif result == '-12' or result == -12:
            return -2
        else:
            return -2
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2

    return 1

def process_ret_106j(sender, param):
    result = 'message send fail'
    try:
        result = param['ret'][2]
        x = parseString(result)
        result = int(x.firstChild.firstChild.data)
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2

    return 1

if __name__ == '__main__':
    for i in range(1, 10):
        xmlString = '''<?xml version="1.0" encoding="utf-8"?>
<string xmlns="http://tempuri.org/">0</string>
'''
        try:
            print xmlString
            x = parseString(xmlString)
            result = int(x.firstChild.firstChild.data)
            print result

            if result == '0' or result == 0:
                print 1
            elif result == '-1' or result == -1:
                print -1
            elif result == '-2' or result == -2:
                print -1
            elif result == '-3' or result == -3:
                print -1
            elif result == '-4' or result == -4:
                print -2
            elif result == '-5' or result == -5:
                print -2
            elif result == '-6' or result == -6:
                print -2
            elif result[1] == '7':#-7
                print -2
            elif result == '-8' or result == -8:
                print -1
            elif result == '-9' or result == -9:
                print -1
            elif result == '-10' or result == -10:
                print -2
            elif result == '-11' or result == -11:
                print -2
            elif result == '-12' or result == -12:
                print -2
            else:
                print -2
        except:
            print_exc()
            print -2

