'''
Created on 2011-4-9

@author: Plato Sun
'''

from dbobj import dbobj

class phonebook(dbobj):
    table_name = 'phonebook'
    fields = 'uid,user_uid,name,remark'
    key = 'uid'


    def __init__(self):
        self.uid = ''
        self.user_uid = ''
        self.name = ''
        self.remark = ''
        
    def new(self, user_uid, name, remark):
        """ new phonebook """
        self.user_uid = user_uid
        self.name = name
        self.remark = remark        
        rows = self.db.raw_sql_query("select %s from %s where user_uid = %s and name = '%s'" %(self.key, self.table_name, user_uid, name) )
        if rows != None and len(rows) > 0:
            return
        self.create()
      
    def from_row(self, uid, user_uid, name, remark):
        """ load from database """
        self.uid = uid
        self.user_uid = user_uid
        self.name = name
        self.remark = remark  
    
    def to_json(self):
        d = {}
        d['uid'] = self.uid
        d['user_uid'] = self.user_uid
        d['name'] = self.name
        d['remark'] = self.remark
        return d