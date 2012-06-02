# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import re

class PhoneNumber(object):
    cm = set(['134', '135', '136', '137', '138', '139', '150', '151', '152',
                '157', '158', '159', '187', '188', '147','182', '183'])
    cu = set(['130', '131', '132', '155', '156', '186', '145'])
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
    def _to_list(cls, ret):
        new_ret = {}
        for key, value in ret.iteritems():
            new_ret[key] = list(value)
            new_ret[key].sort()
        return new_ret
    @classmethod
    def split_addr(cls, addr):
        '''
        split addr_list to {cm:cm_list, cu:cu_list, ct:ct_list}
        '''
        ret = {cls.S_CM:set(), 
               cls.S_CU:set(),
               cls.S_CT:set(),
               cls.S_INVALID:set()}
        
        if isinstance(addr, str):
            addr_list = re.findall('\d*', addr)
            print addr_list
        elif not isinstance(addr, list):
            return cls._to_list(ret)
        else:
            addr_list = addr
            
        try:
            for addr in filter(lambda x: len(x) > 3, addr_list):
                ret[cls.check_addr(addr)].add(addr)
        except:
            pass
        
        return cls._to_list(ret)
        
if __name__ == '__main__':

    
    print PhoneNumber.check_addr('15011325023')
    print PhoneNumber.check_addr('123456')
    print PhoneNumber.check_addr('12345625023')
    print PhoneNumber.check_addr('18900000000')
    ret = PhoneNumber.split_addr(['15011325023','18616820727','18900000000','1890000000','1234'])
    print str(ret)
    print str(PhoneNumber.split_addr('15011325023,18616820727;18988888,123456'))
