'''
Created on 2011-10-5

@author: xbfool
'''
import unittest
from smsd2.context.context import Context

class ContextTest(unittest.TestCase):
    def testContext(self):
        c = Context('testyaml.yaml')
        self.failUnless(c.cfg)
        self.failUnless(c.db)
        self.failUnless(c.meta)
        pass


if __name__ == "__main__":
    unittest.main()