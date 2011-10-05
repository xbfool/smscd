# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

'''
Created on 2011-10-4

@author: xbfool
'''
from sqlalchemy import create_engine

def create_db(cfg):
    db = create_engine('%s://%s:%s@%s/%s' % 
                                  (cfg.database.engine,
                                   cfg.database.user,
                                   cfg.database.password,
                                   cfg.database.host,
                                   cfg.database.db))
    return db
    
    