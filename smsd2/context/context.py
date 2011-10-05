'''
Created on 2011-10-5

@author: xbfool
'''

from smsd2.config.config_reader import loadcfg
from smsd2.database.db_engine import create_meta, create_db
class Context:
    def __init__(self, config_path):
        self.__load_cfg(config_path)
        self.__init_db()
        self.__init_meta()
    
    def __load_cfg(self, config_path):
        self.cfg = loadcfg(config_path)
    
    def __init_db(self):
        self.db = create_db(self.cfg)
    
    def __init_meta(self):
        self.meta = create_meta() 
    
    