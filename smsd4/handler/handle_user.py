__author__ = 'xbfool'

from sqlalchemy import and_, or_
from session import session_get_user
from user import User
from datetime import datetime
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

    if operate_user.uid == dest_user.uid:
        #change pwd by self
        oldp = kargs.get('oldp')
        if oldp != dest_user.password:
            return {'rtype':'changepwd', 'errno':1}

    dest_user.password = newp
    db.commit()
    return {'rtype':'changepwd', 'errno':0}

def handle_adduser(context, kargs):
    db =  context.db

    sid = kargs.get('sid')
    operate_user = session_get_user(context, sid)

    if not (operate_user & User.F_CREATE_USER):
        return {'rtype':'adduser', 'errno':2} #cannot create


    username = kargs.get('user')
    password = kargs.get('pass')
    flags = kargs.get('flags')
    desc = kargs.get('name')
    can_weblogin = kargs.get('can_weblogin')
    can_post = kargs.get('can_post')
    need_check = kargs.get('need_check')
    cm = kargs.get('cm')
    cu = kargs.get('cu')
    ct = kargs.get('ct')

    if db.user.filter(db.user.username == username).count() != 0:
        return {'rtype':'adduser', 'errno': 1} #duplicated username

    if flags & User.F_CHARGE or flags & User.F_CREATE_USER:
        if not (operate_user.flags & User.F_CREATE_USER):
            return False

    if flags & User.F_CREATE_CHARGE:
        if operate_user.username != 'root':
            return False

    if operate_user.username != 'root':
        percent = operate_user.percent
    else:
        percent = 100

    db.user.insert(username = username,
        description = desc,
        password = password,
        parent_id = operate_user.uid,
        msg_num = 0,
        flags = flags,
        is_active = True,
        create_time = datetime.now(),
        last_login = datetime.now(),
        can_weblogin = can_weblogin,
        can_post = can_post,
        need_check = need_check,
        channel_cm = cm,
        channel_cu = cu,
        channel_ct = ct,
        ext = '',
        percent = percent,
        channel_list_id = 0,
        msg_postfix = ''
    )


    return {'rtype':'adduser', 'errno':0}

