'''
Created on 2010-9-5

@author: xbfool
'''

import re

class phonenumber(object):
    cm = set(["134", "135", "136", "137", "138", "139", "150", "151", "152",
                "157", "158", "159", "187", "188", "147","182", "183"])
    cu = set(["130", "131", "132", "155", "156", "186", "145"])
    ct = set(["133", "153", "189", "180", "181"])
    S_CM = 0
    S_CU = 1
    S_CT = 2
    S_INVALID = 100
    def __init__(self):
        pass
    
    def check_addr(self, addr):
        if len(addr) != 11:
            return self.S_INVALID
        p = re.compile('\d*')

        try:
            if p.match(addr) == None:
                return self.S_INVALID
        except:
            return self.S_INVALID
        
        title = addr[0:3]
        if title in self.cm:
            return self.S_CM
        elif title in self.cu:
            return self.S_CU
        elif title in self.ct:
            return self.S_CT
        else:
            return self.S_INVALID 
    
    def split_addr(self, addr_list):
        '''
        split addr_list to {cm:cm_list, cu:cu_list, ct:ct_list}
        '''
        ret = {self.S_CM:[], 
               self.S_CU:[],
               self.S_CT:[],
               self.S_INVALID:[]}
        try:
            for addr in addr_list:
                ret[self.check_addr(addr)].append(addr)
        except:
            pass
        return ret
        
if __name__ == '__main__':
    pm = phonenumber()
    
    print pm.check_addr("15011325023")
    print pm.check_addr("123456")
    print pm.check_addr("12345625023")
    print pm.check_addr("18900000000")
    ret = pm.split_addr(['15011325023',"18900000000",'1890000000','1234'])
    print str(ret)
