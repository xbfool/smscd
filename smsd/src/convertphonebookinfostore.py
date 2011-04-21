'''
Created on 2011-4-21

@author: Plato Sun
'''

from loadcfg import loadcfg
from dbsql import dbsql
from addresslist import addresslist
from phonebook import phonebook
from phone import phone

class convert(object):
    def __init__(self, conf = 'smsd.ini'):        
        self.cfg = loadcfg(conf)        
        self.db = dbsql(**self.cfg.database.raw_dict)
        
    def run(self):
        addresslist.set_db(self.db, "addresslist")
        addresslists = addresslist.load()
        phonebook.set_db(self.db, "phonebook")
        phone.set_db(self.db, "phone")
        for notebook in addresslists:
            user_uid = notebook.user_uid
            name = notebook.name
            number = notebook.number
            list = number.split(";")
            phonebook_new = phonebook()
            phonebook_new.new(user_uid, name, "")
            uid = phonebook_new.uid
            for mobile in list:
                phone_new = phone()
                phone_new.new(uid, "", "", "", mobile)    

if __name__ == '__main__':
    application = convert()
    application.run()