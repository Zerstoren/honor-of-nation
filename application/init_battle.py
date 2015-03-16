from tornado import ioloop

from battle.incomingBattle import IncomingBattle

if __name__ == '__main__':
    try:
        ioloop.IOLoop.instance().start()
    except KeyError:
        ioloop.IOLoop.instance().stop()
