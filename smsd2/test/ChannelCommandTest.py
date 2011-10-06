'''
Created on 2011-10-6

@author: xbfool
'''
import unittest
from smsd2.context.context import Context
from smsd2.command.ChannelCommand import SmsdCommand
from smsd2.database.create_table import create_table
class ChannelCommandTest(unittest.TestCase):
    def setUp(self):
        self.c = Context('sqlite.yaml')
        create_table(self.c.db)
        self.command = SmsdCommand(self.c)
        
    def tearDown(self):
        self.c = None
        self.command = None


    def test_channel_item_add(self):
        ret = self.command(command='channel_item_add',name='name1', desc='desc1', type='abc')
        self.failUnless(self.command.check_ret(ret))
    
if __name__ == "__main__":
    unittest.main()