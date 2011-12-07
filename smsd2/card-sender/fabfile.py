from fabric.api import run, env
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