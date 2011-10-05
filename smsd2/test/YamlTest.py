'''
Created on 2011-10-5

@author: xbfool
'''

import unittest
from smsd2.config.config_reader import loadcfg

class YamlTest(unittest.TestCase):
    def testYaml(self):
        cfg = loadcfg('mysqldb.yaml') 
        self.failUnlessEqual(cfg.smsd.session_expire, 3600)
 
            
if __name__ == '__main__':
    unittest.main()