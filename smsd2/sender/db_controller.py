'''
Created on 2011-10-18

@author: xbfool
'''
from msg_status import msg_status
from traceback import print_exc
def send_success(db, param, result):
    try:
        status = msg_status.F_SEND
        db.raw_sql_wo_commit('UPDATE user SET msg_num = msg_num - %s where uid = %s', \
                                (param['msg_num'], param['user_uid']))
        db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))
    except:
        print_exc()
  
def send_fail(db, param, result):
    try:
        status = msg_status.F_FAIL

        db.raw_sql_wo_commit('UPDATE message SET status = %s, last_update = %s, fail_msg = \"%s\", sub_num = %s where uid = %s', \
                                (status, param['time'], result, param['msg_num'] * param['percent'] / 100, param['uid']))

    except:
        print_exc()
      
