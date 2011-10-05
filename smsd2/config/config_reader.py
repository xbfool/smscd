# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-4

@author: xbfool
'''

from yaml import load
from yaml import Loader
    
def loadcfg(path):
    stream = open(path, 'r')
    data = load(stream, Loader=Loader)
    return data