# -*- coding: utf-8 -*-

'''
Created on 2011-8-10

@author: xbfool
'''

from datetime import datetime
from datetime import timedelta
from copy import copy
from collections import deque

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime

Base = declarative_base()

def is_the_same_hour(dt1, dt2):
    return (dt1.year == dt2.year and
            dt1.month == dt2.month and
            dt1.day == dt2.day and
            dt1.hour == dt2.hour)

def is_the_same_day(dt1, dt2):
    return (dt1.year == dt2.year and
            dt1.month == dt2.month and
            dt1.day == dt2.day)

def is_the_same_month(dt1, dt2):
    return (dt1.year == dt2.year and
            dt1.month == dt2.month)
    
class CardNumber(Base):
    __tablename__ = 'CardNumber'
    '''
    this class manage one card numbers
    '''
    S_OK = 0
    S_STOP = 1
    S_DEL = 2
    status_list = range(3)
    id = Column(Integer, primary_key=True)
    number = Column(String(50), nullable=False, unique=True)
    status = Column(Integer)
    lastupdate = Column(TIMESTAMP)
    hourrate = Column(Integer)
    dayrate = Column(Integer)
    monthrate = Column(Integer)
    
    
    def __init__(self, number,
                 status=0,
                 lastupdate=None,
                 hourrate=0,
                 dayrate=0,
                 monthrate=0):
        
        self.number = number
        self.status = status
        self.lastupdate = lastupdate
        self.hourrate = hourrate
        self.dayrate = dayrate
        self.monthrate = monthrate
    

    def can_send(self, dt=None, hour_max=300, day_max=1000, month_max=30000):
        if dt == None:
            dt = datetime.now()
        if self.lastupdate != None and self.lastupdate > dt:
            return False
        return (self.status == self.S_OK and
            hour_max > self.hourrate and
            day_max > self.dayrate and
            month_max > self.monthrate)
            
    def send_one(self, dt):
        if self.lastupdate == None:
            self.lastupdate = dt
            self.hourrate += 1
            self.dayrate += 1
            self.monthrate += 1
            
        elif self.lastupdate <= dt:
            if is_the_same_hour(dt, self.lastupdate):
                self.hourrate += 1
            else:
                self.hourrate = 0
            if is_the_same_day(dt, self.lastupdate):
                self.dayrate += 1
            else:
                self.dayrate = 0
            if is_the_same_month(dt, self.lastupdate):
                self.monthrate += 1
            else:
                self.monthrate = 0
        else:
            raise Exception()
            


        
    def _change_status(self, status):
        if status not in CardNumber.status_list:
            raise Exception()
        else:
            self.staus = status
            
    def enable(self):
        self._change_status(self.S_OK)
        
    def disable(self):
        self._change_status(self.S_STOP)
        
  
class CardMsgHistory(Base):
    __tablename__ = 'CardSendHistory'
    
    id = Column(Integer, primary_key=True)
    number_id = Column(Integer, ForeignKey('CardNumber.id'))
    create_time = Column(TIMESTAMP)
    msg = Column(String(500))
    dst_number = Column(String(50))
    number = relationship("CardNumber", backref=backref('numbers', order_by=create_time))
    
    def __init__(self, number, dst_number, msg="", create_time=datetime.now()):
        self.number = number
        self.dst_number = dst_number
        self.msg = msg
        self.create_time = create_time
    
class CardPool(object):
    '''
    this class manage sim card numbers
    '''

    
    def __init__(self, max_size=100000, hour_max=300,
                 day_max=1000, month_max=30000):
        '''
        Constructor
        '''
        self.null_number = CardNumber('00000000000')
        self.numbers = {}
        self.hour_max = 300
        self.day_max = 1000
        self.month_max = 30000
        self.avail_list = deque()
        self.max_size = max_size
    
    def add_number_by_string(self, num):
        self.add_number(CardNumber(num))
        
    def add_number(self, card_number):
        if len(self.numbers) < self.max_size:
            self.numbers[card_number.number] = card_number
        
    def enable_number(self, number):
        self.get(number, self.null_number).enable()
        
    def disable_number(self, number):
        self.get(number, self.null_number).disable()
        
    def _get_avail_list(self, dt):
        l = filter((lambda x: x.can_send(dt,
                                         hour_max=self.hour_max,
                                         day_max=self.day_max,
                                         month_max=self.month_max)),
                   self.numbers.values())
        self.avail_list.extend(l)
                                         
    def pop_next_number(self, dt):
        if len(self.avail_list) == 0:
            self._get_avail_list(dt)
        if len(self.avail_list) == 0:
            return None
        else:
            while len(self.avail_list) > 0:
                i = self.avail_list.popleft()
                if i.can_send(dt, hour_max=self.hour_max,
                                day_max=self.day_max,
                                month_max=self.month_max):
                    return i.number
            return None
    
    def update_send_info(self, dt, number):
        self.numbers.get(number, self.null_number).send_one(dt)
            
    def get_next_number(self):
        dt = datetime.now()
        n = self.pop_next_number(dt)
        if n != None:
            self.update_send_info(dt, n)
        return n
