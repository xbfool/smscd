import web
import json
import urllib
from traceback import print_exc
class handler:
    def GET(self):
        get_input = dict(web.input(_method='get'))
        ret_data = self._processor(get_input)
        if get_input.get('rettype') == 'json':
            return self._return_json(ret_data)
        elif get_input.get('rettype') == 'urlencode':
            return self._return_urlencode(ret_data)
        else:
            return ret_data


    def POST(self):
        get_input = web.input(_method='get')
        post_input = web.input(_method='post')
        print post_input.type
        if get_input.get('type') == 'json':
            param = self._parse_json(web.data())
        else:
            param = dict(post_input)
        ret_data = self._processor(param)
        if get_input.get('rettype') == 'json':
            return self._return_json(ret_data)
        elif get_input.get('rettype') == 'urlencode':
            return self._return_urlencode(ret_data)
        else:
            return ret_data
    

    def _processor(self, args):
        return args

    def _parse_json(self, data):
        try:
            print data
            ret = json.loads(data)
            return ret
        except:
            print_exc()
            return None

    def _return_urlencode(self, data):
        print 'in urlencode'
        return urllib.urlencode(data)

    def _return_json(self, data):
        print 'in json'
        return json.dumps(data)


