'''
Created on 2011-10-6

@author: xbfool
'''
import unittest
from smsd2.context.context import Context
from smsd2.command.SmsdCommand import SmsdCommand
from smsd2.database.create_table import create_table
from hashlib import sha1
class SmsdCommandTest(unittest.TestCase):
    def setUp(self):
        self.c = Context('mysqldb.yaml')
        create_table(self.c.db)
        self.command = SmsdCommand(self.c)
        
    def tearDown(self):
        self.c = None
        self.command = None


    def test_channel_item_add(self):
        ret = self.command(command='channel_item_add',name='name1', desc='desc1', type='abc')
        self.failUnless(self.command.check_ret(ret))
    
    def test_user_login(self):
        ret = self.command(command='user_login',username='root', password=sha1('debug').hexdigest())
        self.failUnless(self.command.check_ret(ret))
if __name__ == "__main__":
    unittest.main()