# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-4

@author: xbfool
'''
from sqlalchemy import create_engine
from sqlalchemy import MetaData

def create_db(cfg):
    if(cfg.database.engine == 'mysql+mysqldb'):
        db = create_engine('%s://%s:%s@%s/%s' % 
                                      (cfg.database.engine,
                                       cfg.database.user,
                                       cfg.database.password,
                                       cfg.database.host,
                                       cfg.database.db), 
                                       #echo='debug'
                                       )
    elif(cfg.database.engine == 'sqlitememory'):
        db = create_engine('sqlite://')
    return db

def create_meta():
    meta = MetaData()
    return meta
    