__author__ = 'xbfool'

import sqlsoup

def create_db():
    db =  sqlsoup.SQLSoup('%s://%s:%s@%s/%s' %
                       ('mysql+mysqlconnector',
                        'root',
                        'ftp3*8*ing',
                        '127.0.0.1',
                        'smsd'),
        #echo='debug'
    )
    return db