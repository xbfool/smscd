# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import sys
from threading import Thread, currentThread
# from constants import *
from random import random, seed
from datetime import datetime
from struct import pack, unpack
from types import NoneType
from urllib import unquote_plus

seed(datetime.now())

def isInt(s):
    if s[0] == '-':
        s = s[1:]
    if len(s) < 1:
        return False
    for c in s:
        if c not in '0123456789':
            return False
    return True

def isFloat(s):
    if s[0] == '-':
        s = s[1:]
    if s == '.':
        return False
    dot_found = False
    for c in s:
        if c == '.':
            if dot_found:
                return False
            else:
                dot_found = True
        elif c not in '0123456789':
            return False
    return True

def isHex(s):
    if len(s) < 3:
        return False
    s = s.lower()
    mark = s[:2]
    if mark != '0x':
        return False
    s = s[2:]
    for c in s:
        if c not in '0123456789abcdef':
            return False
    return True

# CAUTION, safeint supports only unsigned int, but returns -1 while error
def safeint(a, silent = True):
    t = type(a)
    #print 'safeint processing \'%s\'%s' %(a, t)
    if t == int:
        return a
    elif t == float:
        return int(a)
    elif t == str:
        if a == '':
            return 0
        elif a.isdigit():
            return int(a)
        #elif isHex(a):
        #    return  
        elif isFloat(a):
            return int(float(a))
    if not silent:
        print 'safeint can\'t convert \'%s\'%s to int, returned -1' % (a, t)
    return -1

def str2value(s):
    if type(s) != str:
        return s
    elif len(s) < 1:
        return s
    elif isInt(s):
        return int(s)
    elif isFloat(s):
        return float(s)
    else:
        return s

def thread_helper_starter(start, arg):
    name = currentThread().getName()
    print '%s thread started' % name
    if arg == None:
        start()
    else:
        start(arg)
    print '%s thread stopped' % name

def thread_helper(start, name = 'anonymous_thread_created_by_thread_helper', arg = None):
    return Thread(None, thread_helper_starter, name, (start, arg))

def token():
    token_f = random()
    token_0, token_1 = unpack('ii', pack('d', token_f))
    return '%08x' % abs(token_0 ^ token_1)

def timedelta2seconds(t):
    return t.days * 60 * 60 * 24 + t.seconds

def seconds2string(sec):
    if sec <= 0:
        return '0秒'
    day = sec / 86400
    hour = sec % 86400 / 3600
    minute = sec % 3600 / 60
    second = sec % 60
    str = ''
    if day > 0:
        str += '%d天' % day
    if hour > 0:
        str += '%d小时' % hour
    if minute > 0:
        str += '%d分' % minute
    if second > 0:
        str += '%d秒' % second
    return str

def dump(v):
    return str(v) + str(type(v))

class listfilter(object):
    def __init__(self, reference_list):
        self.__ref = reference_list
    
    def filter(self, a):
        return a in self.__ref
    
    def reverse_filter(self, a):
        return a not in self.__ref

class logfile(object):
    def __init__(self, console_encoding = 'utf-8', filename = '', log_to_console_too = True, force_flush = False):
        log_file = open('%s.%s.log' % (filename, datetime.now().strftime('%Y-%m-%d.%H.%M.%S')), 'w')
        log_file.write('\xef\xbb\xbf') # UTF-8 BOM
        self.__logfile = log_file
        self.__console = log_to_console_too
        self.__console_encoding = console_encoding
        self.__console_utf8 = self.__console_encoding == 'utf-8'
        self.__force_flush = force_flush
        
    def read(self):
        return None
    
    def write(self, line):
        # deal with naughty print, thus make it thread friendly
        l = len(line)
        if l == 0 or (l == 1 and line == '\n'):
            return
        elif line[-1:] != '\n':
            line += '\n'
        self.__logfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + line)
        if self.__force_flush:
            self.__logfile.flush()
        if self.__console:
            if self.__console_utf8:
                sys.__stdout__.write(line)
            else:
                # make windows console happy
                sys.__stdout__.write(line.decode('utf-8').encode(self.__console_encoding))
            
    def flush(self):
        self.__logfile.flush()
        
    def close(self):
        self.__logfile.close()
        
def bool_helper(s):
    t = type(s)
    if t == str:
        s = s.lower()
        return s != '0' and s != 'off' and s != 'false'
    else:
        return bool(s)

class sortie(object):
    
    def _set_cmpkey(self, cmpkey):
        self._cmpkey = cmpkey
        
    def _get_cmpvalue(self):
        return self.__dict__[self._cmpkey]
    
    def __cmp__(self, other):
        if id(self) == id(other):
            # '===' surely is '=='
            return 0
        if not isinstance(other, sortie):
            # we can't handle this
            return 1
        sv = self._get_cmpvalue()
        ov = other._get_cmpvalue()
        # some value (like datetime) can't be compared to None
        # so we take care of it here
        if type(sv) == NoneType:
            if type(ov) == NoneType:
                # both None, cmp by id
                return cmp(id(self), id(other))
            else:
                # None < anything else
                return -1
        else:
            if type(ov) == NoneType:
                # anything else > None
                return 1
            else:
                # both not None, we can cmp safely
                vcmp = cmp(sv, ov)
                if vcmp == 0:
                    # same value, cmp by id too
                    return cmp(id(self), id(other))
                else:
                    return vcmp

def rec_uni2str(o, encoding = 'utf-8'):
    if isinstance(o, list):
        return map(rec_uni2str, o)
    elif isinstance(o, tuple):
        return tuple(map(rec_uni2str, o))
    elif isinstance(o, dict):
        return dict(zip(map(rec_uni2str, o.keys()), map(rec_uni2str, o.values())))
    elif isinstance(o, unicode):
        return o.encode(encoding)
    else:
        return o

def urldecode(s, retain_duplicate_entries = True):
    # rival for urllib.urlencode
    d = {}
    l = map(lambda e:map(unquote_plus, e.partition('=')), s.split('&'))
    for e in l:
        k = e[0]
        v = e[2]
        ov = d.get(k)
        if ov != None:
            if not retain_duplicate_entries:
                continue
            if isinstance(ov, list):
                d[k].append(v)
            else:
                d[k] = [ov, v]
        else:
            d[k] = v
    return d

if __name__ == '__main__':
    print safeint(1)
    print safeint(1.1)
    print safeint('1')
    print safeint('1.1')
    print safeint('1.1.')
    print safeint('a')
    print safeint((1,))
    for i in range(100):
        print token()
    print dump(str2value('10239485'))
    print dump(str2value('-10239485'))
    print dump(str2value('1.190345'))
    print dump(str2value('-1.190345'))
    print dump(str2value('1.190345.134'))
    print dump(str2value('google.com'))
    print dump(str2value('.'))
    