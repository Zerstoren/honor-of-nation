import sys
import signal
import os
os.chdir(os.path.split(os.path.abspath(__file__))[0])

from system.UserTransfer import UserTransfer
from helpers import times

import exceptions.handler
import system.router
import system.log

import json
import zlib

import balancer.client.respondent

from tornado import ioloop


def handler(content, userId):
    transfer = UserTransfer()

    if userId:
        transfer.setUserById(userId)

    data = False
    try:
        data = json.loads(zlib.decompress(content).decode('utf-8'))
    except Exception:
        transfer.send('/error', {"text": 'Not valid json'})

    if data is False:
        pass

    elif 'collection' not in data:
        execute(transfer, data)

    elif 'collection' in data:
        transfer.startCollect()
        for action in data['collection']:
            execute(transfer, action)

    result = transfer.purge()

    if transfer.hasUser():
        user = str(transfer.getUser().getId())
    else:
        user = None

    return (result, user, )


def execute(transfer, data):
    if 'async' in data:
        transfer.setAsync(data['async'])

    method = system.router.searchExecControllerMethod(data['module'])

    times.start()

    exceptions.handler.handle(method)(transfer, data['message'])

    system.log.debug("%s -\t\t%s sec" % (
        data['module'], str(times.complete())[0:7]
    ))


if __name__ == '__main__':
    balancer.client.respondent.Respondent.setHandler(handler)

    system.log.info("Server is prepared")

    def signal_handler(signal, frame):
        system.log.info('Backend instance get SIGINT')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    ioloop.IOLoop.instance().start()
