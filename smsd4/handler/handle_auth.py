__author__ = 'xbfool'
from hashlib import sha1
from sqlalchemy import and_, or_
from session import session_create

def handle_auth(context, kargs):
    db = context.db
    u = kargs.get('user')
    p = kargs.get('pass')
    session = None
    user = db.user.filter(and_(db.user.username == u, db.user.password == p)).first()
    if user is None:
        p = sha1(p).hexdigest()
        user = db.user.filter(and_(db.user.username == u, db.user.password == p)).first()

    if user is None:
        return {'rtype':'err', 'error':'1'}
    else:
        session = session_create(context, user.username)
        return {'rtype':'auth', 'sid':session.sid, 'username':session.username}