'''
Created on 2011-10-18

@author: xbfool
'''

class msg_status():
    F_ALL = 0
    F_COMMIT = 1
    F_SEND = 2
    F_REJECT = 3
    F_ADMIT = 4
    F_DELETE = 5
    F_CANCEL = 6
    F_FAIL = 7
    F_POST_COMMIT = 8
    
class channel_status():
#    S_OK = 0
#    S_ERROR = 1
#    S_STOP = 2
    S_CM_OK = 0x000
    S_CM_ERROR = 0x001
    S_CM_STOP = 0x002
    S_CM_OK_MASK = 0x003
    S_CM_MASK = 0x330
    S_CU_OK = 0x000
    S_CU_ERROR = 0x010
    S_CU_STOP = 0x020
    S_CU_OK_MASK = 0x030
    S_CU_MASK = 0x303
    S_CT_OK = 0x000
    S_CT_ERROR = 0x100
    S_CT_STOP = 0x200
    S_CT_OK_MASK = 0x300
    S_CT_MASK = 0x033
    
    cm = set(["134", "135", "136", "137", "138", "139", "150", "151", "152",
                "157", "158", "159", "187", "188", "147","182"])
    cu = set(["130", "131", "132", "155", "156", "186", "145"])
    ct = set(["133", "153", "189"])
    
    @classmethod
    def is_channel_ok(cls, status, addr):
        
        title = addr[0:3]
        if title in cls.cm:
            return (cls.S_CM_OK_MASK & status) == cls.S_CM_OK
        elif title in cls.cu:
            return (cls.S_CU_OK_MASK & status) == cls.S_CU_OK
        elif title in cls.ct:
            return (cls.S_CT_OK_MASK & status) == cls.S_CT_OK
     
    @classmethod
    def is_channel_error(cls, status, addr):
        
        title = addr[0:3]
        if title in cls.cm:
            return (cls.S_CM_ERROR & status) == cls.S_CM_ERROR
        elif title in cls.cu:
            return (cls.S_CU_ERROR & status) == cls.S_CU_ERROR
        elif title in cls.ct:
            return (cls.S_CU_ERROR & status) == cls.S_CU_ERROR   
      
    @classmethod
    def is_channel_stop(cls, status, addr):
        
        title = addr[0:3]
        if title in cls.cm:
            return (cls.S_CM_STOP & status) == cls.S_CM_STOP
        elif title in cls.cu:
            return (cls.S_CU_STOP & status) == cls.S_CU_STOP
        elif title in cls.ct:
            return (cls.S_CT_STOP & status) == cls.S_CT_STOP   

    @classmethod
    def start_status(cls, status, addr):
        title = addr[0:3]
        if title in cls.cm:
            return (cls.S_CM_MASK & status) | cls.S_CM_OK
        elif title in cls.cu:
            return (cls.S_CU_MASK & status) | cls.S_CU_OK
        elif title in cls.ct:
            return (cls.S_CT_MASK & status) | cls.S_CT_OK
        
    @classmethod
    def down_status(cls, status, addr):
        title = addr[0:3]
        if title in cls.cm:
            return (cls.S_CM_MASK & status) | cls.S_CM_ERROR
        elif title in cls.cu:
            return (cls.S_CU_MASK & status) | cls.S_CU_ERROR
        elif title in cls.ct:
            return (cls.S_CT_MASK & status) | cls.S_CT_ERROR