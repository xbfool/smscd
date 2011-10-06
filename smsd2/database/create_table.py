from sqlalchemy import MetaData, Table, Column, Integer, String, DefaultClause
from sqlalchemy.types import DateTime
def create_table(db):
    meta = MetaData()
    c = Table('ChannelItem', meta,
        Column('uid', Integer, primary_key = True),
        Column('name', String(50), nullable = False, unique = True),
        Column('desc', String(50)),
        Column('type', String(50), nullable = False),
        Column('status', Integer, DefaultClause("0")),
        Column('last_update', DateTime)
        )

    l = Table('ChannelList', meta,
        Column('uid', Integer, primary_key = True),
        Column('name', String(50), nullable = False, unique = True),
        Column('desc', String(100)),
        Column('cm1', Integer, DefaultClause("-1")),
        Column('cm2', Integer, DefaultClause("-1")),
        Column('cm3', Integer, DefaultClause("-1")),
        Column('cu1', Integer, DefaultClause("-1")),
        Column('cu2', Integer, DefaultClause("-1")),
        Column('cu3', Integer, DefaultClause("-1")),
        Column('ct1', Integer, DefaultClause("-1")),
        Column('ct2', Integer, DefaultClause("-1")),
        Column('ct3', Integer, DefaultClause("-1")),
        )
    tablelist = [c, l]
    meta.create_all(tables = tablelist, bind=db)