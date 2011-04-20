'''
Created on 2011-4-14

@author: Plato Sun
'''

from dbobj import dbobj

class phone(dbobj):
    table_name = 'phone'
    fields = 'uid,phonebook_uid,name,companyname,title,mobile'
    key = 'uid'

    def __init__(self):
        self.uid = ''
        self.phonebook_uid = ''
        self.name = ''
        self.companyname = ''
        self.title = ''
        self.mobile = ''
        
    def new(self, phonebook_uid, name, companyname, title, mobile):
        """ new phone """
        self.phonebook_uid = phonebook_uid
        self.name = name
        self.companyname = companyname
        self.title = title
        self.mobile = mobile
        rows = self.db.raw_sql_query("select %s from %s where phonebook_uid = %s and mobile = '%s'" %(self.key, self.table_name, phonebook_uid, mobile) )
        if rows != None and len(rows) > 0:
            return
        self.create()
                  
    def from_row(self, uid, phonebook_uid, name, companyname, title, mobile):
        """ load from database """
        self.uid = uid
        self.phonebook_uid = phonebook_uid
        self.name = name
        self.companyname = companyname  
        self.title = title
        self.mobile = mobile
    
    def to_json(self):
        d = {}
        d['uid'] = self.uid
        d['phonebook_uid'] = self.phonebook_uid
        d['name'] = self.name
        d['companyname'] = self.companyname
        d['title'] = self.title
        d['mobile'] = self.mobile
        return d
    
    def loadByID(self, phonebook_uid, uid):
        rows = self.db.raw_sql_query("select %s from %s where phonebook_uid = %s and uid = %s" % (self.fields, self.table_name, phonebook_uid, uid))
        if rows != None and len(rows) ==1:
            result = rows[0]
            i = phone()
            i.from_row(*result)
            self.uid = i.uid      
            self.phonebook_uid = i.phonebook_uid     
            self.name = i.name
            self.companyname = i.companyname  
            self.title = i.title
            self.mobile = i.mobile
    
    def deleteByPhonebookUid(self, phonebook_uid):
        self.db.raw_sql_query("delete from %s where phonebook_uid = %s" % (self.table_name, phonebook_uid))
        