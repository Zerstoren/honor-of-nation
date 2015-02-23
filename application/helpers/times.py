import time
import system.log

startTime = 0.0


def start():
    globals()['startTime'] = time.time()


def complete():
    timeItem = time.time() - globals()['startTime']
    globals()['startTime'] = 0
    return timeItem

def timer():
    startTime = time.time()

    def complete():
        timeItem = time.time() - startTime
        return timeItem

    return complete

def decorate(fn):
    def wrapper(*args, **kwards):
        start = time.time()
        result = fn(*args, **kwards)

        text = "Fn %s" % fn.__name__

        if bool(args):
            text += " -> %d args " % len(args)
        if bool(kwards):
            text += " -> %d kwargs " % len(kwards)

        text += "execute in %s" % (time.time() - start)

        system.log.info(text)
        print(text)

        return result
    return wrapper

