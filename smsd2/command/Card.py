from sqlalchemy import MetaData, Table, Column, Integer, String, DefaultClause
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
    
class CardItem(Base):
     __tablename__ = 'card_item'
     uid = Column(Integer, primary_key=True)
     number = Column(String(50))
     type = Column(String(50))
     provider = Column(String(50))
     group_id = Column(Integer)
     total_max = Column(Integer)
     total = Column(Integer)
     month_max = Column(Integer)
     month = Column(Integer)
     day_max = Column(Integer)
     day = Column(Integer)
     hour_max = Column(Integer)
     hour = Column(Integer)
     minute_max = Column(Integer)
     minute = Column(Integer)
     last_send = Column(DateTime)
     due_time = Column(DateTime)
     status = Column(String(50))
     
     def __init__(self, number, type='default', provider='default',
        group_id = 0,
        total_max = 0,
        total = 0,
        month_max = 0,
        day_max = 0,
        day = 0,
        hour_max = 0,
        minute_max = 0,
        minute = 0,
        last_send = datetime.now()):
        self.number = number
        self.type = type
        self.provider = provider
        self.group_id = group_id
        self.total_max = total_max
        self.total = total
        self.month_max = month_max
        self.day_max = day_max
        self.day = day
        self.hour_max = hour_max
        self.minute_max = minute_max
        self.minute = minute
        self.last_send = last_send
