'''
Created on 2011-8-31

@author: Administrator
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://root:123456@localhost/smsd2', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


