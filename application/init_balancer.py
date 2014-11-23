import os
os.chdir(os.path.split(os.path.abspath(__file__))[0])

from tornado import websocket, web, ioloop

import balancer.server.clientConnector
import balancer.server.surveyor
import balancer.server.workerStarter
import balancer.celery_receiver.receiver

import config

class SocketHandler(websocket.WebSocketHandler):
    def open(self):
        self.user = balancer.server.clientConnector.ClientConnector()
        self.user.connect(self)

    def on_message(self, content):
        balancer.server.surveyor.Surveyor.send(self.user, content)

    def on_close(self):
        self.user.disconnect()
        self.user = None

    def check_origin(self, origin):
        return True

app = web.Application([
    ('/', SocketHandler)
])

if __name__ == '__main__':
    app.listen(int(config.get('server.port')), config.get('server.host'))

    workers = balancer.server.workerStarter.Process()
    workers.run()

    try:
        ioloop.IOLoop.instance().start()

    except Exception:
        workers.stop()
