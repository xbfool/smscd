'''
Created on 2011-10-13

@author: xbfool
'''
from CommandUtil import *

def user_login(context, **args):
    user = args['username']
    password = args['password']
    c = context.get_controller('user')
    ret = c.login(user, password)      
    return ret_util(ret)

def user_query_all(context, **args):
    c = context.get_controller('user')
    ret = c.query_all()
    return ret_util(ret)

def user_update_channel_list(context, **args):
    c = context.get_controller('user')
    user_id = args['user_id']
    channel_list_id = args['channel_list_id']
    ret = c.update_channel_list(user_id, channel_list_id)
    return ret_util(ret)