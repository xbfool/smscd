from sqlalchemy import MetaData, Table, Column, Integer, String, DefaultClause
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
carditem = Table('card_item', meta,
    Column('uid', Integer, primary_key = True),
    Column('number', String(50), nullable = False, unique = True),
    Column('type', String(100)),
    Column('provider', String(100)),
    Column('group_id', Integer),
    Column('total_max', Integer),
    Column('total', Integer),
    Column('month_max', Integer),
    Column('month', Integer),
    Column('day_max', Integer),
    Column('day', Integer),
    Column('hour_max', Integer),
    Column('hour', Integer)
    Column('minute_max', Integer),
    Column('minute', Integer)
    Column('last_send', DateTime)
    )
    
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
     last_send = Column(Datetime)
     
     def __init__(self, number, type='defaulte', provider='default',
        group_id = 0,
        total_max = 0,
        total = 0,
        month_max = 0,
        day_max = 0,
        day = 0,
        hour_max = 0,
        minute_max = 0,
        minute = 0
        last_send = datetime.now():
         self.name = name
