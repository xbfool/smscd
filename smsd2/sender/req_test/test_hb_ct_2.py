from zhttp import *
from xml.dom.minidom import parseString

def test_req():
    from time import time
    from hashlib import md5
    t = str(int(time() * 1000))
    apName = 'xghcdrs005'
    apPasswd = 'xu=qwe'
    p = md5('%s%s%s' % ( apName, apPasswd, t)).hexdigest()
    h = zhttp(host='58.53.194.80',
              path='/swdx/services/SmsBizService',
              mode='soap')
    soap = \
        '''
        <soap:Envelope
            xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <SendMessage xmlns="http://trust.me.nobody/cares/this/">
                    <SendMessageRequest>
                        <id>1</id>
                        <compId>%s</compId>
                        <accountId>%s</accountId>
                        <apName>%s</apName>
                        <apPass>%s</apPass>
                        <timeStamp>%s</timeStamp>
                        <calledNumber>%s</calledNumber>
                        <content>%s</content>
                        <smsType>1</smsType>
                    </SendMessageRequest>
                </SendMessage>
            </soap:Body>
        </soap:Envelope>
        ''' \
    % ('xghcdrs1', 'xghcdrs05', apName, p, t, '18616820727', 'test sms from sender') 
    ret = h.send(soapaction='http://58.53.194.80/swdx/services/SmsBizService/', soap=soap)
    #print ret[0]
    #print ret[1]
    #print '\n'.join(map(str, ret[3]))
    #print ret[2]
    process_ret_hb_ct(ret)
def process_ret_hb_ct(ret):
    result = 'message send fail'
    try:
        resultDOM = parseString(ret[2])
        result1 = resultDOM.firstChild.firstChild.firstChild.firstChild.firstChild
        ret1_text = result1.firstChild.data
        result2 = result1.nextSibling
        ret2_text = result2.firstChild.data
        result3 = result2.nextSibling
        ret3_text = result3.firstChild.data
        print ret3_text
        ret = ret2_text.split('-')
        print ret[0]
        if ret[0] == 'SUCC':
            return 1
        else:
            return -1
    except:
        print_exc()
        return -1

    return 1
if __name__ == '__main__':
    test_req()