from fabric.api import run, env, local
from fabric.colors import green
env.hosts = ['sms.xbfool.com']
from fabric.operations import put
def sender1():
    put('sender_util.py', '/tmp/')
    put('sender1.py', '/tmp/')
    run('python2.7 /tmp/sender1.py')
    run('rm /tmp/sender_util.py')
    run('rm /tmp/sender1.py')
    
def sender2():
    put('sender2.py', '/tmp/')
    run('python2.7 /tmp/sender2.py')
    run('rm /tmp/sender2.py')
    
def sender3():
    put('sender3.py', '/tmp/')
    run('python2.7 /tmp/sender3.py')
    run('rm /tmp/sender3.py')
    
    
def sender4():
    put('sender4.py', '/tmp/')
    run('python2.7 /tmp/sender4.py')
    run('rm /tmp/sender4.py')
    
def sender(n):
    put('sender%s.py' % n, '/tmp/')
    run('python2.7 /tmp/sender%s.py' % n)
    run('rm /tmp/sender%s.py' % n)
    
def r(n, pidfile='twistd.pid'):
    put('sender_service%s.tac' % n, '/tmp/')
    try:
        run('kill `cat %s`' % pidfile)
    except:
        run('twistd --pidfile=%s -y /tmp/sender_service%s.tac' % (pidfile, n))
    #run('rm /tmp/sender%s.py' % n)
    
def l(n, pidfile='twistd.pid'):
    try:
        local('kill `cat %s`' % pidfile)
    except:
        pass
    local('twistd --pidfile=%s -n -y sender_service%s.tac' % (pidfile, n))