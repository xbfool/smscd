'''
Created on 2011-10-5

@author: xbfool
'''
import unittest
from smsd2.config.config_reader import loadcfg
from smsd2.database.db_engine import create_db
from sqlalchemy import Column, Integer, Table, MetaData
from traceback import print_exc
class DbTest(unittest.TestCase):
    def testDb(self):
        try:
            cfg= loadcfg('mysqldb.yaml')
            db = create_db(cfg)
            meta = MetaData()
            t = Table('testt', meta,
            Column('uid', Integer, primary_key = True),
            )
            meta.create_all(bind = db, tables =[t])
            self.failUnless(db)
        except:
            print_exc()
            self.fail('testdb Faile')

    def testDbFail(self):
        try:
            cfg= loadcfg('mysqldb.yaml')
            cfg.database.password = '123'
            db = create_db(cfg)
            meta = MetaData()
            t = Table('testt', meta,
            Column('uid', Integer, primary_key = True),
            )
            meta.create_all(bind = db, tables =[t])
            self.failIf(db)
        except:
            pass
        
    def testSqlite(self):
        try:
            cfg= loadcfg('sqlite.yaml')
            db = create_db(cfg)
            self.failIf(db == None)
        except:
            print_exc()
            self.fail('testdb Faile')
if __name__ == "__main__":
    unittest.main()