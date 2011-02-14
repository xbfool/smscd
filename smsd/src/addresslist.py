'''
Created on 2011-1-1

@author: Plato Sun
'''

from dbobj import dbobj

class addresslist(dbobj):
    table_name = 'addresslist'
    fields = 'uid,user_uid,name,number'
    key = 'uid'
    
    def __init__(self):
        self.uid = ''
        self.user_uid = ''
        self.name = ''
        self.number = ''
        
    def new(self, user_uid, name, number):
        """ new addresslist """
        self.user_uid = user_uid
        self.name = name
        self.number = number        
        rows = self.db.raw_sql_query("select %s from %s where user_uid = %s and name = '%s'" %(self.key, self.table_name, user_uid, name) )
        if rows != None and len(rows) > 0:
            return
        self.create()
    
    def from_row(self, uid, user_uid, name, number):
        """ load from database """
        self.uid = uid
        self.user_uid = user_uid
        self.name = name
        self.number = number
    
    def deleteOne(self, user_uid, name):
        rows = self.db.raw_sql_query("select %s from %s where user_uid = %s and name = '%s'" %(self.key, self.table_name, user_uid, name) )
        if rows != None and len(rows) ==1:
            row = rows[0]
            print 'delete one'
            print row
            self.uid = row
            self.delete()
    
    def loadByName(self, user_uid, name):
        rows = self.db.raw_sql_query("select uid,user_uid,name,number from %s where user_uid = %s and name = '%s'" % (self.table_name, user_uid, name))
        if rows != None and len(rows) ==1:
            result = rows[0]
            i = addresslist()
            i.from_row(*result)
            self.number = i.number      
            self.uid = i.uid     
            self.name = i.name
            self.user_uid = i.user_uid
    
    def to_json(self):
        d = {}
        d['uid'] = self.uid
        d['user_uid'] = self.user_uid
        d['name'] = self.name
#        list = split_pattern.split(self.number)
        list = self.number.split(";")
        d['count'] = len(list)
        return d