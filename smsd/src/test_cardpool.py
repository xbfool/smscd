from sqlalchemy import create_engine
from cardpool import *

def test_CardNumber():
    mysql_db = create_engine('mysql+mysqldb://user:123456@localhost/test')
    from sqlalchemy.orm import sessionmaker
    Base.metadata.create_all(mysql_db) 
    Session = sessionmaker(bind=mysql_db)
    session = Session()
    
    
    dt1 = datetime.now()
 
    
    cn = session.query(CardNumber).filter_by(number='15011325023').all()
    if not cn:
        cn = CardNumber('15011325023')
        session.add(cn)
    else:
        cn = cn[0]
    for i in range(200):
        if cn.can_send(datetime.now()):
            cn.send_one(datetime.now())

        
    for i in range(200):
        cmh = CardMsgHistory(cn, "abcde"+str(i))
    session.commit()    
    for num in session.query(CardNumber).all():
        for n in num.numbers:
            print n.dst_number, n.create_time
    session.commit()
    return True

if __name__ == '__main__':
    if test_CardNumber():
        print "the class CardPool test passed"
    else:
        print "the class CardPool test failed"