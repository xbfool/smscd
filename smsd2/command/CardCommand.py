# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-5

@author: xbfool

'''

from CommandUtil import *
from datetime import datetime
from Card import CardItem
from traceback import print_exc

def card_item_add(context, **args):
    new_arg = {}
    for key, value in args.iteritems():
        if key in ('number', 'type', 'provider', 'group_id', 'total_max', 'total',
                    'month_max', 'day_max', 'day', 'hour_max', 'hour',
                    'minute_max', 'minute', 'last_send','due_time'):
            new_arg[key] = value
    try:
        if context.session.query(CardItem).filter_by(number=args.get('number')).count() > 0:
            return ret_util(False, -1, 'the number %s is duplicated' % args.get('number'))
        c = CardItem(**new_arg)
        context.session.add(c)
        context.session.commit()
        return ret_util(True)
    except:
        return ret_util(False)
        
def card_item_delete(context, **args):
    try:
        a = context.session.query(CardItem).filter_by(uid=args.get('uid')).first()
        if a:
            context.session.delete(a)
            context.session.commit()
            return ret_util(True)
        else:
            return ret_util(False, -1, 'the uid %s is not exist' % args.get('uid'))
    except:
        return ret_util(False)

def card_item_update(context, **args):
    try:

        new_arg = {}
        for key, value in args.iteritems():
            if key in ('type', 'provider', 'group_id', 'total_max', 'total',
                        'month_max', 'day_max', 'day', 'hour_max', 'hour',
                        'minute_max', 'minute', 'last_send','due_time'):
                new_arg[key] = value
                
        a = context.session.query(CardItem).filter_by(uid=args.get('uid')).update(new_arg)
        if not a:
            return ret_util(False, -1, 'the uid %s is not exist' % args.get('uid'))

        context.session.commit()
        return ret_util(True)
    except: 
        print_exc()
        return ret_util(False)
        
def card_item_query(context, **args):
    try:
        a = context.session.query(CardItem).all()
        l = list([])
        if a != None:
            for i in a:
                l.append(dict(i.to_dict()))
        return ret_util(l, 0)
    except:
        return ret_util(False)
        