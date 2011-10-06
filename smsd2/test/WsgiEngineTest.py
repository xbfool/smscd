from webtest import TestApp
from webtest import AppError
from smsd2.engine import WsgiEngine

import unittest
from traceback import print_exc

def commandJsonA(**param):
    return {'ret': 'haha return commandJsonA'}
def commandTextA(**param):
    return 'haha return commandTextA'

class WsgiEngineTest(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(WsgiEngine.WsgiEngine)
    
    def tearDown(self):
        self.app = None

    def testNotFound(self):
        try:
            self.app.get('/http404notfound.html')
            self.fail('404 not found test failed')
        except AppError:
            pass
        
    def testAddCommand(self):
        class TestEngine(WsgiEngine.WsgiEngine):
            def __init__(self, env, start_response):
                WsgiEngine.WsgiEngine.__init__(self, env, start_response)
                self.add_command(commandJsonA, '/jsonA', 'json')
        try:
            self.app = TestApp(TestEngine)
            self.app.get('/jsonA')
        except AppError:
            print_exc()
            self.fail('testAddCommandError')
            
    def testAddCommandError(self):
        class TestEngine(WsgiEngine.WsgiEngine):
            def __init__(self, env, start_response):
                WsgiEngine.WsgiEngine.__init__(self, env, start_response)
                self.add_command(commandJsonA, '/jsonA', 'json')
                self.add_command(commandJsonA, '/jsonA', 'json')
        try:
            self.app = TestApp(TestEngine)
            self.app.get('/jsonA')
            self.fail('testAddCommandError')
        except StandardError :
            pass
        
    def testJsonCommand(self):
        class TestEngine(WsgiEngine.WsgiEngine):
            def __init__(self, env, start_response):
                WsgiEngine.WsgiEngine.__init__(self, env, start_response)
                self.add_command(commandJsonA, '/jsonA', 'json')
        try:
            self.app = TestApp(TestEngine)
            res = self.app.get('/jsonA')
            import json
            json.loads(res.body)
        except AppError:
            self.fail('testAddCommandError')
            
            
if __name__ == '__main__':
    unittest.main()