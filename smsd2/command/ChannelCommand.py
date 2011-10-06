# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-5

@author: xbfool

'''
from CommandUtil import *

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

