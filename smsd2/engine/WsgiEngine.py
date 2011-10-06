# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-4

@author: xbfool
'''

import json
from traceback import print_exc
from smsd2.utils.utils import urldecode

class WsgiEngine(object):
    def __init__(self, env=None, start_response=None):
        self.env = env
        self.start = start_response
        self.ret_callback = None
        self.context = None
        self.command_dict = {}
        self.ret_callback = {}
        
        self.init_ret_callback__()
        
        pass
    
    def init_ret_callback__(self):
        self.ret_callback['json'] = self.__ret_json
        self.ret_callback['text'] = self.__ret_text
        
    def __call__(self, env, start_response):
        query = self.__get_query(env)
        c = self.command_dict.get(env['PATH_INFO'])
        if c:
            ret_by_command = c['command'](**query)
            ret_for_client = c['ret_type'](ret_by_command)
            return ret_for_client
        else:
            print_exc()
            return self.__not_found()
    
    def __iter__(self):
        query = self.__get_query(self.env)
        c = self.command_dict.get(self.env['PATH_INFO'])
        if c:
            ret_by_command = c['command'](**query)
            ret_for_client = c['ret_type'](ret_by_command)
            yield ret_for_client
        else:
            print_exc()
            yield self.__not_found()
        
    def __get_query(self, env):
        length = 0
        query = {}
        try:
            length = int(env['CONTENT_LENGTH'])
        except:
            pass
        if length > 0:
            post_data = env['wsgi.input'].read(length)
            try:
                query = urldecode(post_data)
            except:
                query = {}
        return query
    def add_command(self, command, path, ret_type):
        errmsg = ''
        if self.command_dict.get(path):
            errmsg = 'the command path %s  has registered already' % (path)
        elif not callable(command):
            errmsg = 'the command is not callable'
        elif ret_type not in ('json', 'text'):
            errmsg = 'the ret_type: %s is not accept' % (ret_type)
        else:
            self.command_dict[path] = {'command':command,
                                       'path':path,
                                       'ret_type':self.ret_callback[ret_type]}
            return True
        raise(StandardError (errmsg))
    
    def set_context(self, context):
        self.context = context
        
    def __ret_text(self, ret):
        self.start('200 OK', [('Content-type', 'text/plain')])
        return ret
    
    def __ret_json(self, ret):
        self.start('200 OK', [('Content-type', 'application/json')])
        return json.dumps(ret, separators=(',', ':'))
    
    def __not_found(self):
        self.start('404 NOT FOUND', [('Content-type', 'text/plain')])
        return 'Not Found'
