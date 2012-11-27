__author__ = 'xbfool'

from sqlalchemy import and_, or_
from session import session_get_user
from user import User
def handle_changepwd(context, kargs):
    db = context.db

    sid = kargs.get('sid')
    username = kargs.get('username')
    newp = kargs.get('newp')

    operate_user = session_get_user(context, sid)

    dest_user = db.user.filter(db.user.username == username).first()

    if operate_user is None or dest_user is None:
        return {'rtype':'changepwd', 'errno':2} #something is wrong

    if (not User.is_admin(operate_user) and
        not User.is_parent(operate_user, dest_user) and
        not operate_user.uid == dest_user.uid):
        return {'rtype':'changepwd', 'errno':3} #you cannot do it

    if operate_user.uid == dest_user.uid