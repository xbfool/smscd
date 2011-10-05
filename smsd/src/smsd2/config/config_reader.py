# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-4

@author: xbfool
'''

from yaml import load
from yaml import Loader
    
def dict2obj(d):
        if isinstance(d, list):
            d = [dict2obj(x) for x in d]
        if not isinstance(d, dict):
            return d
        class C(object):
            pass
        o = C()
        for k in d:
            o.__dict__[k] = dict2obj(d[k])
        return o
    
def loadcfg(path):
    stream = open(path, 'r')
    data = load(stream, Loader=Loader)
    return dict2obj(data)