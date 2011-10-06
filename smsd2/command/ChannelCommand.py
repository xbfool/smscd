# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-5

@author: xbfool

'''

from smsd2.command.Command import Command
from smsd2.command.Channel import ChannelItemController, ChannelListController

class ChannelCommand(Command):
    def __init__(self, context):
        Command.__init__(self,
                         context,
                         no_command_callback  = self.__none_method_callback__, 
                         command_error_callback = self.__method_error_callback__)
        self.context.set_controller(
                                    channel_item = ChannelItemController(self.context),
                                    channel_list = ChannelListController(self.context)
                                    )
        command_list = [channel_item_add,
                        channel_item_del,
                        channel_item_update,
                        channel_item_query_by_uid,
                        channel_item_query_by_name,
                        channel_item_query_all,
                        channel_list_add,
                        channel_list_del,
                        channel_list_update,
                        channel_list_query_by_uid,
                        channel_list_query_by_name,
                        channel_list_query_all
                        ]
                        
        self.add_all(*command_list)
    
    def __none_method_callback__(self, context, param):
        return {'errno':-1001, 'errtext':'no such method', 'param': param}
    
    def __method_error_callback__(self, context, param):
        return {'errno':-1000, 'errtext':'method exec error', 'param': param}

def ret_util(ret):
    if ret:
        return {'errno': 0, 'errtext':'command exec success', 'value': ret}
    else:
        return {'errno': -1, 'errtext':'command exec failed', 'value': ret}  


def channel_item_add(context, **args):
    new_arg = {}
    for key, value in args.iteritems():
        if key in ['name', 'desc', 'type',
                   'status', 'last_update']:
            new_arg[key] = value
    c = context.get_controller('channel_item')
    ret = c.add(**args)       
    return ret_util(ret)
        
def channel_item_del(context, **args):
    uid = args['uid']
    c = context.get_controller('channel_item')
    ret = c.delete(uid)
    return ret_util(ret)

def channel_item_update(context, **args):
    uid = args['uid']
    values = args['values']
    new_arg = {}
    for key, value in values.iteritems():
        if key in ['name', 'desc', 'type',
                   'status', 'last_update']:
            new_arg[key] = value
    c = context.get_controller('channel_item')
    ret = c.update(uid, **new_arg)
    return ret_util(ret)

def channel_item_query_by_uid(context, **args):
    uid = args['uid']
    c = context.get_controller('channel_item')
    ret = c.query_by_uid(uid)
    return ret_util(ret)

def channel_item_query_by_name(context, **args):
    name = args['uid']
    c = context.get_controller('channel_item')
    ret = c.query_by_name(name)
    return ret_util(ret)

def channel_item_query_all(context, **args):
    c = context.get_controller('channel_item')
    ret = c.query_all()
    return ret_util(ret)

def channel_list_add(context, **args):
    new_arg = {}
    for key, value in args.iteritems():
        if key in ['name', 'desc',
                   'cm1', 'cm2', 'cm3',
                   'cu1', 'cu2', 'cu3',
                   'ct1', 'ct2', 'ct3' ]:
            new_arg[key] = value
    c = context.get_controller('channel_list')
    ret = c.add(**new_arg)       
    return ret_util(ret)
        
def channel_list_del(context, **args):
    uid = args['uid']
    c = context.get_controller('channel_list')
    ret = c.delete(uid)
    return ret_util(ret)

def channel_list_update(context, **args):
    uid = args['uid']
    values = args['values']
    new_arg = {}
    for key, value in values.iteritems():
        if key in ['name', 'desc',
                   'cm1', 'cm2', 'cm3',
                   'cu1', 'cu2', 'cu3',
                   'ct1', 'ct2', 'ct3' ]:
            new_arg[key] = value
    c = context.get_controller('channel_list')
    ret = c.update(uid, **new_arg)
    return ret_util(ret)

def channel_list_query_by_uid(context, **args):
    uid = args['uid']
    c = context.get_controller('channel_list')
    ret = c.query_by_uid(uid)
    return ret_util(ret)

def channel_list_query_by_name(context, **args):
    name = args['uid']
    c = context.get_controller('channel_list')
    ret = c.query_by_name(name)
    return ret_util(ret)

def channel_list_query_all(context, **args):
    c = context.get_controller('channel_list')
    ret = c.query_all()
    return ret_util(ret)

