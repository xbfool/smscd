# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import re
from itertools import islice, starmap
class PhoneNumber(object):
    cm = set(['134', '135', '136', '137', '138', '139', '150', '151', '152',
                '157', '158', '159', '187', '188', '147','182', '183'])
    cu = set(['130', '131', '132', '155', '156', '186', '145', '185'])
    ct = set(['133', '153', '189', '180'])
    S_CM = 0
    S_CU = 1
    S_CT = 2
    S_INVALID = 100
    def __init__(self):
        pass
    
    @classmethod
    def check_addr(cls, addr):
        if len(addr) != 11:
            return cls.S_INVALID
        p = re.compile('\d*')

        try:
            if p.match(addr) == None:
                return cls.S_INVALID
        except:
            return cls.S_INVALID
        
        title = addr[0:3]
        if title in cls.cm:
            return cls.S_CM
        elif title in cls.cu:
            return cls.S_CU
        elif title in cls.ct:
            return cls.S_CT
        else:
            return cls.S_INVALID 
    @classmethod
    def _to_list(cls, ret, count_per_item):
        new_ret = {}
        for key, value in ret.iteritems():
            l = list(value)
            l.sort()
            new_ret[key] = [';'.join(l[i:i+count_per_item])\
                            for i in range(0, len(l), count_per_item)]
            new_ret[key]
        return new_ret
    @classmethod
    def split_addr(cls, addr, count_per_item):
        '''
        addr: 可以是字符串或者list,暂时不支持其他
        count_per_item,数字，每个号码组的号码个数
        '''
        ret = {cls.S_CM:set(), 
               cls.S_CU:set(),
               cls.S_CT:set(),
               cls.S_INVALID:set()}
        
        if isinstance(addr, str):
            addr_list = re.findall('\d*', addr)
            print addr_list
        elif not isinstance(addr, list):
            return cls._to_list(ret, count_per_item)
        else:
            addr_list = addr
            
        try:
            for addr in filter(lambda x: len(x) > 3, addr_list):
                ret[cls.check_addr(addr)].add(addr)
        except:
            pass
        
        return cls._to_list(ret, count_per_item)
        
if __name__ == '__main__':

    
    print PhoneNumber.check_addr('15011325023')
    print PhoneNumber.check_addr('123456')
    print PhoneNumber.check_addr('12345625023')
    print PhoneNumber.check_addr('18900000000')
    ret = PhoneNumber.split_addr(['15011325023','18616820727','18900000000','1890000000','1234'], 1)
    print str(ret)
    print str(PhoneNumber.split_addr('15011325023,15011325022,15011325024,18616820727;18988888,123456', 3))
