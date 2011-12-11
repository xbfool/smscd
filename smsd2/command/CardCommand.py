# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-5

@author: xbfool

'''

from CommandUtil import *
from datetime import datetime
from Card import CardItem

def card_item_add(context, **args):
    new_arg = {}
    for key, value in args.iteritems():
        if key in ('number', 'type', 'provider', 'group_id', 'total_max', 'total',
                    'month_max', 'day_max', 'day', 'hour_max', 'hour',
                    'minute_max', 'minute', 'last_send')
            new_arg[key] = value
    try:        
        c = CardItem(**new_arg)
        context.session.add(c)
        return ret_util(True)
    except:
        return ret_util(False)
        
