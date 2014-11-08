import os
os.chdir(os.path.split(os.path.abspath(__file__))[0])

from tornado import websocket, web, ioloop

import balancer.clientConnector
import balancer.surveyor
import balancer.workerStarter

import config

class SocketHandler(websocket.WebSocketHandler):
    def open(self):
        self.user = balancer.clientConnector.ClientConnector()
        self.user.connect(self)

    def on_message(self, content):
        balancer.surveyor.Surveyor.send(self.user, content)

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

    workers = balancer.workerStarter.Process()
    workers.run()

    try:
        import tornado.stack_context
        import contextlib
        import sys

        @contextlib.contextmanager
        def die_on_error():
            try:
                yield
            except Exception:
                print("exception in asynchronous operation")
                sys.exit(1)

        with tornado.stack_context.StackContext(die_on_error):
            ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        workers.stop()
