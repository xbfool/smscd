from CommandUtil import *

def user_login(context, **args):
    user = args['username']
    password = args['password']
    c = context.get_controller('user')
    ret = c.login(user, password)      
    return ret_util(ret)
