__author__ = 'xbfool'


class User:
    F_CHARGE                = 0x00000001 # right to charge msg_num to anybody
    F_CREATE_USER           = 0x00000002 # right to create child
    F_CREATE_CHARGE         = 0x00000004

    @classmethod
    def is_admin(cls, u):
        if u.flags == cls.F_CHARGE | cls.F_CREATE_CHARGE | cls.F_CREATE_USER:
            return True
        else:
            return False


    @classmethod
    def is_parent(cls, p, c):
        return c.parentid == c.uid
