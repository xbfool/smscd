def foo1(*args):
    for i in args:
        print i
        
def foo2(**args):
    for i, j in args.iteritems():
        print i, j

def foo3(**args):
    foo2(**args)
    
class foo(object):
    pass
if __name__ == '__main__':
    foo1(1,2,3,4)
    foo2(a=1, b=2, c=3)
    d = {'a':4, 'b':5, 'c':6}
    foo1(*d)
    foo2(**d)
    foo3(**d)
    a = foo()
    try:
        b = a.d
    except AttributeError:
        a.d = 1
