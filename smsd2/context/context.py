'''
Created on 2011-10-5

@author: xbfool
'''

from smsd2.config.config_reader import loadcfg

class Context:
    def __init__(self, config_path):
        self.cfg = self.__load_cfg(config_path)
        self.db = self.__init_db()
    
    def __load_cfg(self, config_path):
        self.cfg = loadcfg(config_path)
    
    def __init_db(self):
        pass
    
    