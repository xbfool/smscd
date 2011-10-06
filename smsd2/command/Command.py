# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-5

@author: xbfool

'''

from traceback import print_exc

class Command(object):
    def __init__(self, context, 
                 ret_callback = None,
                 no_command_callback = None, 
                 command_error_callback = None,
                 dispatch_callback = None,
                 check_ret_callback = None):
        self.dictc = {}
        self.context = context
        self.no_command_callback = no_command_callback
        self.command_error_callback = command_error_callback
        self.ret_callback = ret_callback
        
        if ret_callback:
            self.ret_callback = ret_callback
        else:
            self.ret_callback = self.__default_ret
            
        if dispatch_callback:
            self.dispatch_callback = dispatch_callback
        else:
            self.dispatch_callback = self.__default_dispatch
            
        if check_ret_callback:
            self.__check_ret_callback = check_ret_callback
        else:
            self.__check_ret_callback = self.__default_check_ret
    def add(self, name, callback):
        if self.dictc.get(name):
            raise Exception('the %s command is duplicated', name)
        else:
            self.dictc[name] = callback
        
    def add_all(self, *func_list, **func_dict):
        for i in func_list:
            self.add(i.__name__, i)
        for k, v in func_dict:
            self.add(k, v)
            
    def check_ret(self, ret):
        return self.__check_ret_callback(ret)
        
    def __call__(self, **param):
        c = self.dispatch_callback(**param)
        if c:
            try:
                return c(self.context, **param)
            except:
                print_exc()
                if self.command_error_callback:
                    return self.command_error_callback(self.context, param)
                else:
                    return None

        else:
                if self.no_command_callback:
                    return self.no_command_callback(self.context, param)
                else:
                    return None
    
    def __default_dispatch(self, **param):
        try:
            c = param['command']
            return self.dictc.get(c)
        except:
            return None 
        
    def __default_ret(self, param, **ret):
        r = {}
        for k, v in ret.iteritems():
            r[k] = v
        r['req_param'] = param
        r['command'] = param['command']
        return r
    
    def __default_check_ret(self, ret):
        if ret['errno'] == 0:
            return True
        else:
            return False