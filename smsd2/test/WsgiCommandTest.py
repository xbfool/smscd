from webtest import TestApp
from smsd2.engine import WsgiEngine
from smsd2.command.SmsdCommand import SmsdCommand
from smsd2.context.context import Context
from smsd2.database.create_table import create_table
import json
import unittest


class WsgiEngineTest(unittest.TestCase):
    def setUp(self):
        class TestEngine(WsgiEngine.WsgiEngine):
            def __init__(self, env, start_response):
                WsgiEngine.WsgiEngine.__init__(self, env, start_response)
                self.c = Context('sqlite.yaml')
                create_table(self.c.db)
                self.add_command(SmsdCommand(self.c), '/channel', 'json')
        self.app = TestApp(TestEngine)
    
    def tearDown(self):
        self.app = None

#    def testCommandchannel_item_add(self):
#        ret = self.app.post('/channel', {'command': 'channel_item_add', 'name':'name1', 'desc':'desc1', 'type':'abc'})
#        self.failUnless(json.loads(ret.body)['errno'] == 0)
#        
            
if __name__ == '__main__':
    unittest.main()