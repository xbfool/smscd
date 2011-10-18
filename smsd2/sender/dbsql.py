# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

# dbdata.py provides the dbobj class which contains high level interface for game data operation
#     and dblog class for log

from time import sleep
from traceback import print_exc

class dbengine(object):
    def __init__(self, retry = 3, delay = 10, **kargs):
        self.retry = retry
        self.delay = 10
        self.params = kargs
        self.try_connect()
        
    def connect(self):
        # basic connect method should be provided in sub class
        pass
    
    def format_exc(self, exc):
        pass
    
    def try_connect(self):
        connected = False
        i = 0
        while i < self.retry:
            i += 1
            if i > 1:
                print 'dbengine: connect attempt %d ...' % i
            try:
                self.conn = self.connect()
                connected = True
                break
            except:
                print 'dbengine: connect attempt %d failed, wait %d seconds to retry ...' % (i, self.delay)
                print_exc()
            sleep(self.delay)
        assert connected, 'dbengine: FATAL ERROR: connect failed'
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.cursor.close()
        self.cursor = None
        self.conn.close()
        self.conn = None
    
    def reconnect(self):
        print 'dbengine: reconnecting...'
        self.close()
        self.try_connect()
        print 'dbengine: successfully reconnected'
    
    def execute_wo_reconnect(self, sql, params):
        if params == None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)

    def execute(self, sql, params):
        try:
            self.execute_wo_reconnect(sql, params)
            return True
        except Exception as exc:
            print \
                '=== dbengine: %s, exception dump:\n' \
                '%s\n' \
                'sql:\t%s\n' \
                'params:\t%s\n' \
                '=== dbengine exception dump end' \
                % (exc.__class__.__name__,
                   self.format_exc(exc),
                   sql,
                   isinstance(params, (list, tuple)) and ', '.join(map(str, params)) or 'None')
            if isinstance(exc, (self.db_api.InterfaceError, self.db_api.OperationalError)):
                print 'dbengine: try to reconnect...'
                self.reconnect()
                self.execute_wo_reconnect(sql, params)
                return True
            else:
                return False
        
    def raw_sql(self, sql, params = None):
        if self.execute(sql, params):
            self.conn.commit()
            return self.cursor.rowcount
        else:
            return 0
        
    def raw_sql_wo_commit(self, sql, params = None):
        return self.execute(sql, params)
        
    def raw_commit(self):
        self.conn.commit()
    
    def raw_sql_query(self, sql, params = None):
        # read only queries
        if self.execute(sql, params):
            return self.cursor.fetchall()
        else:
            return None
    

class dbengine_MySQLdb(dbengine):
    @classmethod
    def cls_init(cls):
        if hasattr(cls, 'cls_init_flag'):
            return
        
        import MySQLdb as db_api
        import MySQLdb.converters as converters
        cls.db_api = db_api
        
        cls.place_holder = '%s'
        
        cls.conv = converters.conversions
        # custom converters, this is just an example
        # cls.conv[datetime] = lambda d, dict: converters.Thing2Literal(str(d)[:-7], dict)
        
        cls.cls_init_flag = True
    
    def connect(self):
        self.__svr_name = self.params.get('host')
        if self.__svr_name == None:
            self.__svr_name = '(host name unknown)'
        self.__db_name = self.params.get('db')
        if self.__db_name == None:
            self.__db_name = '(database name unknown)'
            
        conn = self.db_api.connect(conv = self.conv, **self.params)
        print 'dbengine_MySQLdb: successfully connected to %s/%s' \
            % (self.__svr_name, self.__db_name)
        return conn
    
    def format_exc(self, exc):
        return 'MySQLdb: ' + str(exc)
    
    def raw_sql_query(self, sql, params = None):
        # mysql need commit on query on its default isolation level ...
        # http://bytes.com/topic/python/answers/446805-mysqldb-query-fetch-dont-return-result-when-theorically-should
        try:
            self.raw_commit()
        except:
            # raw_commit will fail when the connection was dead
            # simply ignore it will be fine since raw_sql_query will try to reconnect
            # and on that scenario no commit was required
            pass
        return dbengine.raw_sql_query(self, sql, params)
    
 
class dbsql(object):
    """ wrapper class for different dbengine classes """
    def __init__(self, engine, **kargs):
        dbengine_cls = eval(compile('dbengine_%s' % engine, '<string>', 'eval'))
        dbengine_cls.cls_init()
        self.__dbengine = dbengine_cls(**kargs)
        self.place_holder = dbengine_cls.place_holder
        self.raw_sql = self.__dbengine.raw_sql
        self.raw_sql_wo_commit = self.__dbengine.raw_sql_wo_commit
        self.raw_commit = self.__dbengine.raw_commit
        self.raw_sql_query = self.__dbengine.raw_sql_query
    

def __dbsql_tester():
    from loadcfg import loadcfg
    cfg = loadcfg('smsd.ini')
    # d = dbsql(**cfg.pyodbc_test.raw_dict)
    d = dbsql(**cfg.pyodbc_test.raw_dict)
    # print d.raw_sql_query('SELECT * FROM not_exist')
    # sleep(10)
    print d.raw_sql_query('SELECT * FROM user')
    print d.raw_sql('INSERT INTO user(uid,username) VALUES(%s,%s)', (1, 'root'))
    pass

def __dbsql_loop_tester():
    from loadcfg import loadcfg
    cfg = loadcfg('smsd.ini')
    # d = dbsql(**cfg.pyodbc_test.raw_dict)
    d = dbsql(**cfg.database.raw_dict)
    while True:
        r = d.raw_sql_query('SELECT uid from tmp WHERE status = 0')
        if len(r) == 0:
            sleep(1)
            continue
        for l in  r:
            print 'found record:', l[0]
            d.raw_sql('UPDATE tmp SET status = 1 WHERE uid = %s', l[0])

if __name__ == '__main__':
    __dbsql_tester()
    # __dbsql_loop_tester()