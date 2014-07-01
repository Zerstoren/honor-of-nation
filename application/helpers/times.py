import time

startTime = 0.0


def start():
    globals()['startTime'] = time.time()


def complete():
    timeItem = time.time() - globals()['startTime']
    globals()['startTime'] = 0
    return timeItem


def decorate(fn):
    def wrapper(*args, **kwards):
        start()
        result = fn(*args, **kwards)

        text = "Fn %s" % fn.__name__

        if bool(args):
            text += " -> %d args " % len(args)
        if bool(kwards):
            text += " -> %d kwargs " % len(kwards)

        text += "execute in %s" % complete()

        print(text)

        return result
    return wrapper
