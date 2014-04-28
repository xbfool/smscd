'''
Created on 2011-10-18

@author: xbfool
'''

from xml.dom.minidom import parseString

from traceback import print_exc
def process_ret_shangxintong(sender, param):
    success_str = '<Result>1</Result>'
    result = "something is error"
    try:
        resultDOM = parseString(param['ret'][2])
        result = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild.nextSibling.firstChild.data

        
        if result[0] == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        else:
            return -2
            
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2
  
    return -2

def process_ret_qixintong2012(sender, param):
    result = "something is error"
    try:
        result = param['ret'][2]
        rl = result.split(',')

        if rl[1] == '0':
            sender.msg_controller.send_success(param, result)
            return 1
        elif result in ('1', '2', '3', '4', '5', '6', '7', '8'):
            return -2
        elif result in ('9', '11', '15', '16', '17', '21', '99'):
            return -2
        else:
            return -2
            
    except:
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2
    
    return -2

def process_ret_106f(sender, param):
    result = "something is error"
    try:
        xmlString = param['ret'][2]
        xmlStringNoEncoding = xmlString.replace('encoding="gbk"', ' ')
        resultDOM = parseString(xmlStringNoEncoding)
        result = resultDOM.firstChild.firstChild.firstChild.data

        if result in ('00', '01', '03'):
            sender.msg_controller.send_success(param, result)
            return 1
        elif result in ('06', '07', '08', '09', '10', '97', '98', '99'):
            return -2
        elif result in ('02', '04', '05'):
            return -1
        else:
            return -2

    except:
        import string
        success_str = '<code>03</code>'
        try:
            if string.find(param['ret'][2], success_str):
                sender.msg_controller.send_success(param, result)
                return 1
        except:
            print_exc() 
        print_exc()
        sender.msg_controller.send_fail(param, result)
        return -2

    return -2

if __name__ == '__main__':
    for i in range(1, 100000):
        xmlString = '<?xml version="1.0" encoding="gbk" ?><response><code>01</code></response>'
        xmlStringNoEncoding = xmlString.replace('encoding="gbk"', ' ')
        x = parseString(xmlStringNoEncoding)
        result =  x.firstChild.firstChild.firstChild.data
        if result in ('00', '01', '03'):
            print 1
        elif result in ('06', '07', '08', '09', '10', '97', '98', '99'):
            print 2
        elif result in ('02', '04', '05'):
            print 3
        else:
            print 4
