__author__ = 'xbfool'
from hashlib import sha1
import time
from sqlalchemy import and_

SESSION_EXPIRE_TIME = 86400

def session_check(context, username, sid):
    db = context.db
    user = db.user.filter(db.user.username == username).count()
    if user == 0:
        return False

    current_time = time.time()
    session = db.sessions.filter(and_(db.sessions.username == username, db.sessions.sid == sid,
        db.sessions.active > current_time - SESSION_EXPIRE_TIME)).first()

    if session is None:
        return False
    else:
        return True

def session_create(context, username):
    db = context.db
    user = db.user.filter(db.user.username == username).first()
    if user is None:
        return None

    current_time = time.time()
    sid_sha1 = sha1(user.username)
    sid_sha1.update(user.password)
    sid_sha1.update(str(current_time))

    session = db.sessions.filter(db.sessions.username == user.username).first()
    if session is None:
        session = db.sessions.insert(username = user.username, sid = sid_sha1.hexdigest(), active = current_time)
    else:
        session.sid = sid_sha1.hexdigest()
        session.active = current_time

    db.commit()

    return session

def session_get_user(context, sid):
    db = context.db
    s = db.sessions.filter(db.sessions.sid == sid).first()
    if s is None:
        return None

    user = db.user.filter(db.user.username == s.username).first()

    return user


