import simplejson as json
import copy
import httplib, urllib
#from ..setting.settings import settings

def send(channel, addr, msg, settings):
    s = copy.copy(settings[channel])
    s['params']['phone']= addr
    s['params']['message']= msg.decode('utf8').encode(s['config']['encoding'])
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    params = urllib.urlencode(s['params'])
    conn = httplib.HTTPConnection(host=s['site']['host'],port=s['site']['port'])
    conn.request(s['site']['mode'], s['site']['path'], params, headers)
    response = conn.getresponse()
    return response.read().decode('gbk')
    

if __name__ == '__main__':
    ret = send('honglian_ty','18616820727','abc')
    print ret