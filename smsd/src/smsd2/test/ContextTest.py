'''
Created on 2011-10-5

@author: xbfool
'''
import unittest
from smsd2.context.context import Context

class ContextTest(unittest.TestCase):
    def testMysqldb(self):
        c = Context('mysqldb.yaml')
        self.failUnless(c.cfg)
        self.failUnless(c.db)
        self.failUnless(c.meta)
    
    def testSqlite(self):
        c = Context('sqlite.yaml')
        self.failUnless(c.cfg)
        self.failUnless(c.db)
        self.failUnless(c.meta)

if __name__ == "__main__":
    unittest.main()