import os
os.chdir(os.path.split(os.path.abspath(__file__))[0])

from tornado import websocket, web, ioloop

from system.UserTransfer import UserTransfer
from helpers import times

import exceptions.handler
import system.router
import config

import json
import subprocess


class SocketHandler(websocket.WebSocketHandler):

    def open(self):
        self.user = UserTransfer()
        self.user.connect(self)

    def on_message(self, content):
        try:
            data = json.loads(content)
        except Exception:
            self.user.send('/error', {"text": 'Not valid json'})
            return

        if 'collection' not in data:
            self.execute(data)

        elif 'collection' in data:
            self.user.startCollect()
            for action in data['collection']:
                self.execute(action)
            self.user.purge()

    def execute(self, data):
        if 'async' in data:
            self.user.setAsync(data['async'])

        method = system.router.searchExecControllerMethod(data['module'])

        times.start()

        exceptions.handler.handle(method)(self.user, data['message'])

        print("%s-\t\t%s sec" % (
            data['module'], str(times.complete())[0:7]
        ))

    def on_close(self):
        self.user = None
    
    def check_origin(self, origin):
        return True

app = web.Application([
    ('/', SocketHandler)
])

if __name__ == '__main__':
    managedProcess = subprocess.Popen([
        'python3',
        '-B',
        'init_celery.py',
        '--type=dev'
    ])

    app.listen(int(config.get('server.port')), config.get('server.host'))

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        managedProcess.terminate()
