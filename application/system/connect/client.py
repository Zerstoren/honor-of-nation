import itertools

import tornado.gen
import tornado.concurrent
import tornado.ioloop
import tornado.iostream
import tornado.tcpclient

import time

import system.log

SOCKET_END = b"\r\n\r\n"


class TCPWrapper(tornado.tcpclient.TCPClient):
    def __init__(self, host, port):
        super().__init__(None, None)
        self.host = host
        self.port = port
        self.connectToServer()

    def connectToServer(self):
        system.log.info('Connect to %s:%s' % (self.host, self.port, ))
        future = self.connect(self.host, self.port)
        future.add_done_callback(self.handle_stream)

    @tornado.gen.coroutine
    def handle_stream(self, future):
        if future.exception():
            self.onClose()
            return

        self.stream = future.result()

        if self._connect_listener:
            self._connect_listener(self)

        self.stream.set_close_callback(self.onClose)
        self.dispatch()

    @tornado.gen.coroutine
    def write(self, data):
        @tornado.gen.coroutine
        def a(d):
            pass

        future = self.stream.write(data + SOCKET_END)
        future.add_done_callback(a)

    @tornado.gen.coroutine
    def dispatch(self):
        try:
            while True:
                msg = yield self.read_until(SOCKET_END)

                if self._read_listener:
                    self._read_listener(self, msg)

        except tornado.iostream.StreamClosedError as e:
            system.log.critical(e)
        return

    @tornado.gen.coroutine
    def read_until(self, delimiter, _idalloc=itertools.count()):
        cb_id = next(_idalloc)
        cb = yield tornado.gen.Callback(cb_id)
        self.stream.read_until(delimiter, cb)
        result = yield tornado.gen.Wait(cb_id)
        raise tornado.gen.Return(result)

    def onClose(self):
        time.sleep(2)
        system.log.warn('Disconnected from %s:%s, try reconnect' % (self.host, self.port, ))
        self.connectToServer()

    _connect_listener = None
    def setConnectListener(self, fn):
        self._connect_listener = fn

    _read_listener = None
    def setReadListener(self, fn):
        self._read_listener = fn

    _close_listener = None
    def setCloseListener(self, fn):
        self._close_listener = fn
