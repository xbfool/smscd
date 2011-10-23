'''
Created on 2011-10-19

@author: xbfool
'''
from base64 import b64encode
from zlib import compress


def process_req_hb_ct(http_pool, setting, msg):
    soap = \
'''
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <SendMessage xmlns="http://trust.me.nobody/cares/this/">
            <ApName>%s</ApName>
            <ApPassword>%s</ApPassword>
            <compcode>%s</compcode>
            <userCode>%s</userCode>
            <calledNumber>%s</calledNumber>
            <sendTime>%s</sendTime>
            <content>%s</content>
        </SendMessage>
    </soap:Body>
</soap:Envelope>
''' \
    % (setting['apid'], 
       setting['appwd'], 
       setting['entid'], 
       setting['uid'],
       ','.join(msg['addr']), 
       '', 
       msg['content'])
    
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'],
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  soapaction='http://58.53.194.80/swdx/services/APService',
                  soap=soap)
    
def process_req_sd_ct(http_pool, setting, msg):
    address_list = msg['addr']
    address_f = [address_list[i] for i in range(len(address_list)) if address_list[i][0:3] != '182']
    if len(address_f) > 0:
        http_pool.req(msg['channel'], 
                      {'user_uid':msg['user_uid'], 
                       'setting':setting, 
                       'uid':msg['uid'], 
                       'msg_num':msg['msg_num'], 
                       'percent':msg['percent']},
                      address=';'.join(address_f), 
                      content=msg['content'], 
                      uid=setting['uid'],
                      pwd=setting['pwd'])
    else:
        http_pool.req(msg['channel'],
                      {'user_uid':msg['user_uid'], 
                       'setting':setting, 
                       'uid':msg['uid'], 
                       'msg_num':msg['msg_num'], 
                       'percent':msg['percent']},
                      address=';'.join(msg['addr']), 
                      content=msg['content'], 
                      uid=setting['uid'],
                      pwd=setting['pwd'])

def process_req_honglian(http_pool, setting, msg):
    if not msg.get['ext']:
        http_pool.req(msg['channel'],
                  {'user_uid':msg['user_uid'], 
                            'setting':setting, 
                            'uid':msg['uid'], 
                            'msg_num':msg['msg_num'],
                             'percent':msg['percent']},
                  phone=','.join(msg['addr']), 
                  message=msg['content'].decode('utf8').encode('gbk'),
                  username=setting['username'],
                  password=setting['password'], 
                  epid=setting['epid']
            )
    else:
        http_pool.req(msg['channel'],
                      {'user_uid':msg['user_uid'], 
                                'setting':setting, 
                                'uid':msg['uid'], 
                                'msg_num':msg['msg_num'],
                                 'percent':msg['percent']},
                      phone=','.join(msg['addr']), 
                      message=msg['content'].decode('utf8').encode('gbk'),
                      username=setting['username'],
                      password=setting['password'], 
                      epid=setting['epid'],
                      subcode=msg['ext'],
                )

def process_req_hlyd(http_pool, setting, msg):
    soap = \
        '''
        <soap:Envelope
            xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <sendSmsAsNormal xmlns="http://trust.me.nobody/cares/this/">
                    <phone>%s</phone>
                    <msgcont>%s</msgcont>
                    <spnumber>%s</spnumber>
                    <chid>%s</chid>
                    <cpid>%s</cpid>
                    <cppwd>%s</cppwd>
                </sendSmsAsNormal>
            </soap:Body>
        </soap:Envelope>
        ''' \
        % (','.join(msg['addr']),
           msg['content'], 
           '', 
           '',
           setting['cpid'], 
           setting['cppwd'])
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  soapaction='http://hl.my2my.cn/services/esmsservice',
                  soap=soap)   
    
def process_req_shangxintong(http_pool, setting, msg):

    soap = \
        '''
        <SOAP:Envelope xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mes="http://message.scape.gsta.com" xmlns:mul="http://www.muleumo.org" xmlns:sms="http://sms.cap.scape.gsta.com" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP:Header xmlns:Header="Header"/>
            <SOAP:Body>
                <mul:sendSMS>
                <mul:in0>
                <mes:account>%s</mes:account>
                <mes:extendField/>
                <mes:hashCode/>
                <mes:password>%s</mes:password>
                <mes:timestamp/>
                </mul:in0>
                <mul:in1>
                <mes:account/>
                <mes:id/>
                </mul:in1>
                <mul:in2>
                <sms:content>%s</sms:content>
                <sms:contentFormat>1</sms:contentFormat>
                <sms:needFeedback>1</sms:needFeedback>
                <sms:password/><sms:receivers>
                <mul:string>%s</mul:string>
                </sms:receivers><sms:areacode/>
                <sms:sender/>
                </mul:in2>
                </mul:sendSMS>
            </SOAP:Body>
        </SOAP:Envelope>
        '''\
        % (setting['account'],
           setting['password'],
           msg['content'],
           ','.join(msg['addr']))
                    
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  soapaction='sendSMS',
                  soap=soap, 
                  port=8081)   
    
def process_req_changshang_a(http_pool, setting, msg):
                      
    tmpmsg = unicode(msg['content'], 'utf-8')
    sendmsg = msg['content']
    try:
        sendmsg = tmpmsg.encode('gbk')
    except:
        pass
    if msg['ext'] == None or msg['ext'] == '':  
        http_pool.__zhttp_pool.req(msg['channel'],
                              {'user_uid':msg['user_uid'], 
                               'setting':setting, 
                               'uid':msg['uid'], 
                               'msg_num':msg['msg_num'], 
                               'percent':msg['percent']},
                              corp_id=setting['corp_id'], 
                              corp_pwd=setting['corp_pwd'], 
                              corp_service=setting['corp_service'],
                              mobile=';'.join(msg['addr']), 
                              msg_content=sendmsg)
    else:
        http_pool.req(msg['channel'], 
                      {'user_uid':msg['user_uid'], 
                       'setting':setting, 
                       'uid':msg['uid'], 
                       'msg_num':msg['msg_num'], 
                       'percent':msg['percent']},
                      corp_id=setting['corp_id'], 
                      corp_pwd=setting['corp_pwd'], 
                      corp_service=setting['corp_service'], 
                      ext=msg['ext'],
                      mobile=msg['addr'], 
                      msg_content=sendmsg)

def process_req_dongguan_0769(http_pool, setting, msg):
                        
    msgtext = \
        '''
        <Ms c=\"1\">
          <m>
            <FA/>
            <FD>%s</FD>
            <FM>%s</FM>
            <FT/>
            <NR/>
        </Ms>
        ''' \
        % (','.join(msg['addr']), 
           msg['content'])
                    
    soap = \
        '''
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <Sms_SendEx2 xmlns="http://tempuri.org/">
              <CompCode></CompCode>
              <UserName>%s</UserName>
              <UserPwd>%s</UserPwd>
              <SendMsgXML>%s</SendMsgXML>
              <withfollow>%s</withfollow>
            </Sms_SendEx>
          </soap:Body>
        </soap:Envelope>
        ''' \
        % (setting['UserName'], 
           setting['UserPwd'], 
           b64encode(compress(msgtext)), 0)
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  soapaction='http://61.145.168.234:90/Interface.asmx',
                  soap=soap)  

def process_req_maoming_ct(http_pool, setting, msg):
    tmpmsg = unicode(msg['content'], 'utf-8')
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  srcmobile=setting['srcmobile'], 
                  password=setting['password'],
                  objmobiles=','.join(msg['addr']), 
                  smstext=tmpmsg.encode('gbk'), rstype='text')
    
def process_req_scp_0591(http_pool, setting, msg):
    address_shu = '|'.join(msg['addr'])
    tmpmsg = unicode(msg['content'], 'utf-8')
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  Mobile=address_shu, 
                  MsgContent=tmpmsg.encode('gbk'))
    