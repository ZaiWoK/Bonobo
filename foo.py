def wrapper(f):
    def wrapped(*args):
        print("Entry: %s" % args)
        v = f(*args)
        print ("Result : %s" % v)
        return v
    return wrapped

@wrapper
def f(x):
    return x+1

# @wrapper == f=wrapper(f)