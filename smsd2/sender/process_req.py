'''
Created on 2011-10-19

@author: xbfool
'''
from base64 import b64encode
from zlib import compress
import hashlib
import time

def safe_utf8_2_gbk(s):
    d = ''
    tmp = s.decode('utf8')
    
    for i in tmp:
        try:
            d += str(i.encode('gbk'))
        except:
            d += '.'
    return d  

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
                   'percent':msg['percent'],
                   'sub_num':msg['sub_num']},
                  soapaction='http://58.53.194.80/swdx/services/APService',
                  soap=soap)

def process_req_hb_ct_2(http_pool, setting, msg):
    from time import time
    from hashlib import md5
    t = str(int(time() * 1000))
    p = md5('%s%s%s' % (  setting['apid'], setting['appwd'], t)).hexdigest()
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
      % (
         setting['entid'], 
         setting['uid'],
         setting['apid'], 
         p, 
         t,
         ','.join(msg['addr']), 
           msg['content'])
    http_pool.req(msg['channel'], 
                {'user_uid':msg['user_uid'],
                'setting':setting, 
                'uid':msg['uid'], 
                'msg_num':msg['msg_num'], 
                'percent':msg['percent'],
                'sub_num':msg['sub_num']},
                soapaction='http://58.53.194.80/swdx/services/SmsBizService/',
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
                       'sub_num':msg['sub_num'], 
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
                       'sub_num':msg['sub_num'],
                       'percent':msg['percent']},
                      address=';'.join(msg['addr']), 
                      content=msg['content'], 
                      uid=setting['uid'],
                      pwd=setting['pwd'])
import phonenumber
import string
def process_req_honglian(http_pool, setting, msg):
    msg_num = ((len(msg['content'].decode('utf8')) - 1) / 64 + 1) * len(msg['total_addr'])
    sub_num =  ((len(msg['content'].decode('utf8')) - 1) / 64 + 1) * len(msg['addr'])
    msg['sub_num'] = sub_num
    pm = phonenumber.phonenumber()

    
    if pm.check_addr(msg['addr'][0]) == pm.S_CM and setting['name'] in ('honglian_ty',):
        new_msg = string.replace(msg['content'], '%', '%25') 
    else:
        new_msg = msg['content']
    
    send_msg = safe_utf8_2_gbk(new_msg)
    if not msg.get('ext') or msg.get('ext') == None  or msg.get('ext') == "":
        http_pool.req(msg['channel'],
                  {'user_uid':msg['user_uid'], 
                            'setting':setting, 
                            'uid':msg['uid'], 
                            'msg_num':msg_num,
                            'sub_num':msg['sub_num'],
                             'percent':msg['percent']},
                  phone=','.join(msg['addr']), 
                  message=send_msg,
                  username=setting['username'],
                  password=setting['password'], 
                  epid=setting['epid']
            )
    else:
        http_pool.req(msg['channel'],
                      {'user_uid':msg['user_uid'], 
                                'setting':setting, 
                                'uid':msg['uid'], 
                                'msg_num':msg_num,
                                'sub_num':msg['sub_num'],
                                 'percent':msg['percent']},
                      phone=','.join(msg['addr']), 
                      message=send_msg,
                      username=setting['username'],
                      password=setting['password'], 
                      epid=setting['epid'],
                      subcode=msg['ext'],
                )

def process_req_honglian1(http_pool, setting, msg):
    msg_num = ((len(msg['content'].decode('utf8')) - 1) / 64 + 1) * len(msg['total_addr'])
    sub_num =  ((len(msg['content'].decode('utf8')) - 1) / 64 + 1) * len(msg['addr'])
    msg['sub_num'] = sub_num
    pm = phonenumber.phonenumber()


    if pm.check_addr(msg['addr'][0]) == pm.S_CM and setting['name'] in ('honglian_ty',):
        new_msg = string.replace(msg['content'], '%', '%25')
    else:
        new_msg = msg['content']

    send_msg = safe_utf8_2_gbk(new_msg)
    if not msg.get('ext') or msg.get('ext') == None  or msg.get('ext') == "":
        http_pool.req(msg['channel'],
            {'user_uid':msg['user_uid'],
             'setting':setting,
             'uid':msg['uid'],
             'msg_num':msg_num,
             'sub_num':msg['sub_num'],
             'percent':msg['percent']},
            phone=','.join(msg['addr']),
            message=send_msg,
            username=setting['username'],
            password=setting['password'],
            epid=setting['epid']
        )
    else:
        http_pool.req(msg['channel'],
            {'user_uid':msg['user_uid'],
             'setting':setting,
             'uid':msg['uid'],
             'msg_num':msg_num,
             'sub_num':msg['sub_num'],
             'percent':msg['percent']},
            phone=','.join(msg['addr']),
            message=send_msg,
            username=setting['username'],
            password=setting['password'],
            epid=setting['epid'],
            subcode=msg['ext'],
        )
def process_req_hlyd(http_pool, setting, msg):
    from hashlib import md5
    p = md5(setting['password']).hexdigest()
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 350:
        if char_num <= 70:
            single_num = 1
        else:
            single_num = (char_num - 1) / 67 + 1
    else:
        single_num = 0
    tmpmsg = safe_utf8_2_gbk(msg['content'])

    http_pool.req(msg['channel'],
                  {'user_uid':msg['user_uid'],
                   'setting':setting,
                   'uid':msg['uid'],
                   'msg_num':msg['msg_num'],
                   'sub_num':msg['sub_num'],
                   'percent':msg['percent']},
                  user=setting['user'],
                  password=p,
                  tele=','.join(msg['addr']),
                  msg=tmpmsg) 
    
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
                   'sub_num':msg['sub_num'],
                   'percent':msg['percent']},
                  soapaction='sendSMS',
                  soap=soap, 
                  port=8081)   

 
        
def process_req_changshang_a(http_pool, setting, msg):
    msg_str_len = len(msg['content'].decode('utf8'))

    if msg_str_len <= 70:
        msg_num =  len(msg['total_addr'])
        msg['sub_num'] = len(msg['addr'])
    else:
        msg_num = ((msg_str_len - 1) / 67 + 1) * len(msg['total_addr'])
        msg['sub_num'] = ((msg_str_len - 1) / 67 + 1) * len(msg['addr'])
                  

    sendmsg = safe_utf8_2_gbk(msg['content'])

    if not msg.get('ext') or msg['ext'] == None or msg['ext'] == '':  
        http_pool.req(msg['channel'],
                              {'user_uid':msg['user_uid'], 
                               'setting':setting, 
                               'uid':msg['uid'], 
                               'msg_num':msg_num, 
                               'sub_num':msg['sub_num'],
                               'percent':msg['percent']},
                              corp_id=setting['corp_id'], 
                              corp_pwd=setting['corp_pwd'], 
                              corp_service=setting['corp_service'],
                              mobile=','.join(msg['addr']), 
                              msg_content=sendmsg)
    else:
        http_pool.req(msg['channel'], 
                      {'user_uid':msg['user_uid'], 
                       'setting':setting, 
                       'uid':msg['uid'], 
                       'msg_num':msg_num, 
                       'sub_num':msg['sub_num'],
                       'percent':msg['percent']},
                      corp_id=setting['corp_id'], 
                      corp_pwd=setting['corp_pwd'], 
                      corp_service=setting['corp_service'], 
                      ext=msg['ext'],
                      mobile=','.join(msg['addr']), 
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
                   'sub_num':msg['sub_num'],
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  soapaction='http://61.145.168.234:90/Interface.asmx',
                  soap=soap)  

def process_req_maoming_ct(http_pool, setting, msg):
    tmpmsg = safe_utf8_2_gbk(msg['content'])
    
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg['msg_num'], 
                   'sub_num':msg['sub_num'],
                   'percent':msg['percent']},
                  srcmobile=setting['srcmobile'], 
                  password=setting['password'],
                  objmobiles=','.join(msg['addr']), 
                  smstext=tmpmsg, rstype='text')
    
def process_req_scp_0591(http_pool, setting, msg):
    address_shu = '|'.join(msg['addr'])
    tmpmsg = safe_utf8_2_gbk(msg['content'])
    #tmpmsg = msg['content']
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'sub_num':msg['sub_num'],
                   'msg_num':msg['msg_num'], 
                   'percent':msg['percent']},
                  Mobile=address_shu, 
                  MsgContent=tmpmsg)
from urllib import urlencode
def process_req_qixintong2012(http_pool, setting, msg):
    msg_num = ((len(msg['content'].decode('utf8')) - 1) / 66 + 1) * len(msg['total_addr'])
    sub_num =  ((len(msg['content'].decode('utf8')) - 1) / 66 + 1) * len(msg['addr'])
    #tmpmsg = safe_utf8_2_gbk(msg['content'])
    tmpmsg = msg['content']
    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg_num, 
                   'sub_num':sub_num,
                   'percent':msg['percent']},
                  uid=setting['uid'],
                  pwd=setting['pwd'],
                  mobiles=','.join(msg['addr']),
                  msg=tmpmsg)
def process_req_zhangshangtong(http_pool, setting, msg):
    msg_str_len = len(msg['content'].decode('utf8'))

    if msg_str_len <= 70:
        msg_num =  len(msg['total_addr'])
        sub_num = len(msg['addr'])
    else:
        msg_num = ((msg_str_len - 1) / 67 + 1) * len(msg['total_addr'])
        sub_num = ((msg_str_len - 1) / 67 + 1) * len(msg['addr'])

    http_pool.req(msg['channel'], 
                  {'user_uid':msg['user_uid'], 
                   'setting':setting, 
                   'uid':msg['uid'], 
                   'msg_num':msg_num, 
                   'sub_num':sub_num,
                   'percent':msg['percent']},
                  ececcid=setting['ececcid'], 
                  password=setting['password'],
                  msgtype=setting['msgtype'],
                  longcode=msg['ext'],
                  msisdn=','.join(msg['addr']), 
                  smscontent=msg['content'])

def process_req_106f(http_pool, setting, msg):
    msg_num = ((len(msg['content'].decode('utf8')) - 1) / 67 + 1) * len(msg['total_addr'])
    sub_num =  ((len(msg['content'].decode('utf8')) - 1) / 67 + 1) * len(msg['addr'])
    tmpmsg = safe_utf8_2_gbk(msg['content'])
    http_pool.req(msg['channel'],
        {'user_uid':msg['user_uid'],
         'setting':setting,
         'uid':msg['uid'],
         'msg_num':msg_num,
         'sub_num':sub_num,
         'percent':msg['percent']},
        OperID=setting['OperID'],
        OperPass=setting['OperPass'],
        DesMobile=','.join(msg['addr']),
        Content=tmpmsg,
        ContentType=8)

def process_req_cmpp_web(http_pool, setting, msg):
    msg_num = ((len(msg['content'].decode('utf8')) - 1) / 67 + 1) * len(msg['total_addr'])
    sub_num =  ((len(msg['content'].decode('utf8')) - 1) / 67 + 1) * len(msg['addr'])

    http_pool.req(msg['channel'],
        {'user_uid':msg['user_uid'],
         'setting':setting,
         'uid':msg['uid'],
         'msg_num':msg_num,
         'sub_num':sub_num,
         'percent':msg['percent']},
        username=setting['username'],
        password=setting['password'],
        msg_id=msg['uid'],
        phone_numbers=','.join(msg['addr']),
        content=msg['content'])

def process_req_106g(http_pool, setting, msg):
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 70:
        single_num = 1
    elif char_num <= 134:
        single_num = 2
    else:
        single_num = 0
    sendmsg = safe_utf8_2_gbk(msg['content'])
    msg_num = single_num * len(msg['total_addr'])
    sub_num = single_num * len(msg['addr'])
    #TODO add http send
    http_pool.req(msg['channel'],
        {'user_uid':msg['user_uid'],
         'setting':setting,
         'uid':msg['uid'],
         'msg_num':msg_num,
         'sub_num':sub_num,
         'percent':msg['percent']},
        Account=setting['account'],
        Password=setting['password'],
        Phones=','.join(msg['addr']),
        Channel=setting['channel'],
        Content=sendmsg)

def process_req_106ha(http_pool, setting, msg):
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 350:
        single_num = (char_num - 1) / 63 + 1
    else:
        single_num = 0

    msg_num = single_num * len(msg['total_addr'])
    sub_num = single_num * len(msg['addr'])
    #TODO add http send
    http_pool.req(msg['channel'],
        {'user_uid':msg['user_uid'],
         'setting':setting,
         'uid':msg['uid'],
         'msg_num':msg_num,
         'sub_num':sub_num,
         'percent':msg['percent']},
        zh=setting['zh'],
        mm=setting['mm'],
        hm=';'.join(msg['addr']),
        nr=msg['content'],
        extno='',
        dxlbid=setting['dxlbid'])

def process_req_106hb(http_pool, setting, msg):
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 350:
        single_num = (char_num - 1) / 65 + 1
    else:
        single_num = 0

    msg_num = single_num * len(msg['total_addr'])
    sub_num = single_num * len(msg['addr'])
    #TODO add http send
    http_pool.req(msg['channel'],
        {'user_uid':msg['user_uid'],
         'setting':setting,
         'uid':msg['uid'],
         'msg_num':msg_num,
         'sub_num':sub_num,
         'percent':msg['percent']},
        zh=setting['zh'],
        mm=setting['mm'],
        hm=';'.join(msg['addr']),
        nr=msg['content'],
        extno='',
        dxlbid=setting['dxlbid'])

def process_req_106j(http_pool, setting, msg):
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 350:
        if char_num <= 70:
            single_num = 1
        else:
            single_num = (char_num - 1) / 67 + 1
    else:
        single_num = 0

    msg_num = single_num * len(msg['total_addr'])
    sub_num = single_num * len(msg['addr'])

    http_pool.req(msg['channel'],
        {'user_uid':msg['user_uid'],
         'setting':setting,
         'uid':msg['uid'],
         'msg_num':msg_num,
         'sub_num':sub_num,
         'percent':msg['percent']},
        userid=setting['userid'],
        account=setting['account'],
        password=setting['password'],
        mobile=','.join(msg['addr']),
        content=msg['content'],
        extno='',
        action='send',
        sendTime='')

def process_req_106k(http_pool, setting, msg):
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 350:
        if char_num <= 70:
            single_num = 1
        else:
            single_num = (char_num - 1) / 67 + 1
    else:
        single_num = 0
    tmpmsg = safe_utf8_2_gbk(msg['content'])

    http_pool.req(msg['channel'],
                  {'user_uid':msg['user_uid'],
                   'setting':setting,
                   'uid':msg['uid'],
                   'msg_num':msg['msg_num'],
                   'sub_num':msg['sub_num'],
                   'percent':msg['percent']},
                  password=setting['password'],
                  to=' '.join(msg['addr']),
                  text=tmpmsg,
                  subid='',
                  msgtype='1')

def process_req_106i(http_pool, setting, msg):
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 350:
        if char_num <= 70:
            single_num = 1
        else:
            single_num = (char_num - 1) / 67 + 1
    else:
        single_num = 0
    tmpmsg = safe_utf8_2_gbk(msg['content'])
    p = hashlib.md5(setting['password']).hexdigest()
    http_pool.req(msg['channel'],
                  {'user_uid':msg['user_uid'],
                   'setting':setting,
                   'uid':msg['uid'],
                   'msg_num':msg['msg_num'],
                   'sub_num':msg['sub_num'],
                   'percent':msg['percent']},
                  userid=setting['userid'],
                  username=setting['username'],
                  passwordMd5=p,
                  #Ext=setting['ext'],
                  mobile=','.join(msg['addr']),
                  message=tmpmsg)

def process_req_lanjing(http_pool, setting, msg):
    print 'process_req_lanjing'
    char_num = len(msg['content'].decode('utf8'))
    single_num = 1
    if char_num <= 350:
        if char_num <= 70:
            single_num = 1
        else:
            single_num = (char_num - 1) / 67 + 1
    else:
        single_num = 0

    msg_num = single_num * len(msg['total_addr'])
    sub_num = single_num * len(msg['addr'])

    seed = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    p1 = str.lower(hashlib.md5(setting['password']).hexdigest())
    p2 = str.lower(hashlib.md5(p1 + seed).hexdigest())
    http_pool.req(msg['channel'],
                  {'user_uid':msg['user_uid'],
                   'setting':setting,
                   'uid':msg['uid'],
                   'msg_num':msg_num,
                   'sub_num':sub_num,
                   'percent':msg['percent']},
                  name=setting['name'],
                  seed=seed,
                  key=p2,
                  dest=','.join(msg['addr']),
                  content=msg['content'])
