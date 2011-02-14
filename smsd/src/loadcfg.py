# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from ConfigParser import ConfigParser
from codecs import EncodedFile

from utils import *

class cfg_section():
    def __init__(self, items):
        self.dict = {}
        self.raw_dict = {}
        for item in items:
            k = item[0]
            v = str2value(item[1])
            self.__dict__[k] = v
            self.dict[k] = v
            self.raw_dict[k] = item[1]

class loadcfg():
    def __init__(self, filename, codepage = 'gbk'):
        cfgparser = ConfigParser()
        print 'loading config from: ' + filename
        f = open(filename)
        if codepage != None and codepage != 'utf-8':
            f = EncodedFile(f, 'utf-8', codepage)
        cfgparser.readfp(f)
        self.section = {}
        for section in cfgparser.sections():
            s = cfg_section(cfgparser.items(section))
            self.__dict__[section] = s
            self.section[section] = s

class csvcfg():
    def __init__(self, csv):
        for name in csv:
            self.__dict__[name] = str2value(csv[name][1])
            
if __name__ == '__main__':
    from os import getcwd
    c = loadcfg(getcwd() + '/config.ini')
    pass