# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

class dbobj(object):
    # sub-class need these
    table_name = ''
    fields = ''
    key = ''
    
    @classmethod
    def set_db(cls, db, table_name):
        """ init class """
        cls.db = db
        
        fields = cls.fields.split(',')
        
        cls.load_sql = 'SELECT %s FROM %s' % (cls.fields, cls.table_name)
        
        fields.remove(cls.key) # primary key is generated in database
        cls.create_sql = 'INSERT INTO %s(%s) VALUES(%s)' % \
            (cls.table_name, ','.join(fields), ','.join([cls.db.place_holder] * len(fields)))
        code = ','.join(map(lambda f: 'self.' + f, fields))
        cls.create_params = compile(code, '<string>', 'eval')
        cls.create_identity = compile('self.%s = key' % cls.key, '<string>', 'exec')
        
        cls.delete_sql = 'DELETE FROM %s WHERE %s = %%s' % \
            (cls.table_name, cls.key)
        cls.delete_params = compile('self.' + cls.key, '<string>', 'eval')
        
        cls.save_sqls = {}

    @classmethod
    def load(cls, where = None, params = None):
        """ batch load from database """
        ret = []
        if where == None:
            rows = cls.db.raw_sql_query(cls.load_sql)
        else:
            rows = cls.db.raw_sql_query(cls.load_sql + ' WHERE ' + where, params)
        if rows != None and len(rows) > 0:
            for row in rows:
                i = cls()
                i.from_row(*row)
                ret.append(i)
        return ret
    
    def create(self):
        """ insert into database """
        self.db.raw_sql(self.create_sql, eval(self.create_params))
        key = self.db.raw_sql_query('SELECT @@IDENTITY')[0][0]
        exec(self.create_identity)
    
    def save(self, fields = None):
        """ update database """
        if fields == None:
            fields = self.fields
        save_sql = self.__class__.save_sqls.get(fields)
        
        if save_sql == None:
            # print 'creating new sql to save: %s' % fields
            f_array = fields.split(',')
            if self.key in f_array:
                f_array.remove(self.key)
            sql_set = ','.join(map(lambda f: f + '=' + self.db.place_holder, f_array))
            sql = 'UPDATE %s SET %s WHERE %s = %s' % \
                (self.table_name, sql_set, self.key, self.db.place_holder)
            code = ','.join(map(lambda f: 'self.' +f, f_array)) + ',self.' + self.key
            params = compile(code, '<string>', 'eval')
            
            self.__class__.save_sqls[fields] = sql, params
        else:
            # print 'pre-compiled sql found to save: %s' % fields
            sql, params = save_sql
        
        self.db.raw_sql(sql, eval(params))
    
    def delete(self):
        """ delete from data base """
        self.db.raw_sql(self.delete_sql, eval(self.delete_params))
        