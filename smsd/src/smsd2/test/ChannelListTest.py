'''
Created on 2011-10-5

@author: xbfool
'''
import unittest
from smsd2.context.context import Context
from smsd2.command.Channel import ChannelListController , CreateChannelListTable
class ChannelTest(unittest.TestCase):
    def setUp(self):
        self.c = Context('sqlite.yaml')
        CreateChannelListTable(self.c.meta, self.c.db)
        self.channel = ChannelListController(self.c)
        
    def tearDown(self):
        self.c = None
        self.channel = None


    def testInsert(self):
        ret = self.channel.add(name='name1', desc='desc1')
        self.failUnless(ret)
    
    def testInsertUnique(self):
        self.channel.add(name='name1', desc='desc1') 
        self.failIf(self.channel.add(name='name1', desc='desc1'))
                    
    def testQuery(self):
        self.channel.add(name='name1', desc='desc1')
        res = self.channel.query_by_name('name1')
        self.failUnless(res)
        a = res
        self.failUnless(a.name == 'name1')
        self.failUnless(a.desc == 'desc1')
    
    def testQueryByUid(self):
        self.channel.add(name='name1', desc='desc1')
        res = self.channel.query_by_uid(1)
        self.failUnless(res)
        a = res
        self.failUnless(a.name == 'name1')
        self.failUnless(a.desc == 'desc1') 
        
    def testDelete(self):
        self.channel.add(name='name1', desc='desc1')
        self.failUnless(self.channel.delete(1))
        res = self.channel.query_by_uid(1)
        self.failIf(res)
    
    def testUpdate(self):
        self.channel.add(name='name1', desc='desc1')
        self.failUnless(self.channel.update(1, name='name2'))
        self.failUnless(self.channel.query_by_uid(1))
        a = self.channel.query_by_name('name2')
        self.failUnless(a.name == 'name2')
    def testQueryAll(self):
        self.channel.add(name='name1', desc='desc1')
        self.channel.add(name='name2', desc='desc2')
        self.channel.add(name='name3', desc='desc3')
        a = self.channel.query_all()
        self.failUnless(len(a) == 3)
        
if __name__ == "__main__":
    unittest.main()