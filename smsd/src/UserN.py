from Utility import *
from datetime import date, datetime, timedelta

class UserN(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    username = Column(String(50))
    description = Column(String(50))
    password = Column(String(40))
    parent_id = Column(Integer)
    msg_num = Column(Integer)
    flags = Column(Integer)
    is_active = Column(Integer)
    create_time = Column(DateTime)
    last_login = Column(DateTime)
    can_weblogin = Column(Integer)
    can_post = Column(Integer)
    need_check = Column(Integer)
    channel_cm = Column(String(4000))
    channel_cu = Column(String(4000))
    channel_ct = Column(String(4000))
    ext = Column(String(50))
    percent = Column(Integer)
    
    # user right flags
    F_CHARGE                = 0x00000001 # right to charge msg_num to anybody
    F_CREATE_USER           = 0x00000002 # right to create child
    F_CREATE_CHARGE         = 0x00000004 
        
    def __init__(self, username, description, password, parent_id, msg_num, can_weblogin, 
            can_post, need_check, 
            channel_cm,
            channel_cu,
            channel_ct,flags = 0, percent = 100):
        
        self.username = username
        self.description = description
        self.password = password
        self.parent_id = parent_id
        self.msg_num = msg_num
        self.flags = flags
        self.is_active = 1
        self.create_time = datetime.now()
        self.last_login = None
        if can_weblogin:
            self.can_weblogin = 1
        else:
            self.can_weblogin = 0
        if can_post:
            self.can_post = 1
        else:
            self.can_post = 0
        if need_check:
            self.need_check = 1
        else:
            self.need_check = 0
        self.channel_cm = channel_cm
        self.channel_cu = channel_cu
        self.channel_ct = channel_ct        
        self.children = {}
        self.commit_num = 0
        self.ext = '' 
        self.percent = percent
        
    def __auth(self, password):
        return self.password == password and self.is_active == 1
    
    def web_auth(self, password):
        return self.__auth(password) and self.can_weblogin
    
    def post_auth(self, password):
        return self.__auth(password) and self.can_post
    
    def change_weblogin_flag(self, flag):
        self.can_weblogin = flag
        
    def change_post_flag(self, flag):
        self.can_post = flag
    
    def change_check_flag(self, flag):
        self.need_check = flag
        
    def change_password(self, password):
        self.password = password
        
    def add_message(self, num):
        self.msg_num = self.msg_num + num
        
    def set_status(self, status):
        self.is_active = status
        
    def add_child(self, child):
        self.check_property()
        self.children[child.username] = child    
    
    def check_property(self):
        if self.children == None:
            self.children = {}
        if self.commit_num == None:
            self.commit_num = 0
    
    def change_info(self, desc, flags, can_weblogin, can_post, need_check):
        self.description = desc
        self.flags = flags
        if can_weblogin:
            self.can_weblogin = 1
        else:
            self.can_weblogin = 0
      
        if can_post:
            self.can_post = 1
        else:
            self.can_post = 0      

        if need_check:
            self.need_check = 1
        else:
            self.need_check = 0
                
    def change_cm(self, cm):
        if self.channel_cm != cm:
            self.channel_cm = cm
            
    def change_cu(self, cu):
        if self.channel_cu != cu:
            self.channel_cu = cu
    
    def change_ct(self, ct):
        if self.channel_ct != ct:
            self.channel_ct = ct            
        
    def change_cm_r(self, cm):
        self.change_cm(cm)
        for u in self.children.itervalues():
            u.change_cm_r(cm)
    
    def change_cu_r(self, cu):
        self.change_cu(cu)
        for u in self.children.itervalues():
            u.change_cu_r(cu)
    
    def change_ct_r(self, ct):
        self.change_ct(ct)
        for u in self.children.itervalues():
            u.change_ct_r(ct)
    
    def set_ext(self,ext):
        self.ext = ext
    
    def is_admin(self):
        return self.flags == UserN.F_CHARGE | UserN.F_CREATE_CHARGE | UserN.F_CREATE_USER
    
    def is_user(self):
        return self.flags == 0
    
    def is_agent(self):
        return self.flags == UserN.F_CHARGE | UserN.F_CREATE_USER    
        
    def delete_child(self, child):
        self.check_property()
        session = Session()
        del self.children[child.username]
        child.delete_allchildren()
        self.add_message(child.msg_num)
        session.delete(child)
        session.commit()

    def delete_allchildren(self):
        self.check_property()
        session = Session()
        for c in self.children:
            c.delete_allchildren()
            session.delete(c)
        self.children = {}
        session.close()
        session.commit()
        
    def to_json(self):
        self.check_property()
        d = {}
        d['uid'] = self.uid
#        print self.uid
        d['parent_id'] = self.parent_id
        d['username'] = self.username
        d['description'] = self.description
        d['msg_num'] = self.msg_num
        d['flags'] = self.flags
        d['is_active'] = self.is_active
        d['create_time'] = self.create_time.strftime("%y-%m-%d %H:%M")
        d['is_can_weblogin'] = self.can_weblogin
        d['is_can_post'] = self.can_post
        d['is_need_check'] = self.need_check
        d['cm'] = self.channel_cm
        d['cu'] = self.channel_cu
        d['ct'] = self.channel_ct
        d['commit_num'] = self.commit_num
        d['ext'] = self.ext
        d['percent'] = self.percent
        if self.last_login == None:
            d['last_login'] = None
        else:
            d['last_login'] = self.last_login.strftime("%y-%m-%d %H:%M")
        return d
    
    def to_json_all(self):
#        print 'to json all'
#        print self.uid
#        print 'begin to print child'
        d = self.to_json()
        
        l = []
        for i in self.children.itervalues():
            l.append(i.to_json_all())
        d['children'] = l
        return d