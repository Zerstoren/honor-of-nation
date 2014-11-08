import itertools

import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.tcpclient


class TCPWrapper(tornado.tcpclient.TCPClient):
    def __init__(self, host, port):
        super().__init__(None, None)
        future = self.connect(host, port)
        future.add_done_callback(self.handle_stream)

    @tornado.gen.coroutine
    def handle_stream(self, future):
        self.stream = future.result()

        if self._connect_listener:
            self._connect_listener(self)

        self.dispatch()

    @tornado.gen.coroutine
    def write(self, data):
        @tornado.gen.coroutine
        def a(d):
            pass

        future = self.stream.write(data + b"\x00\xFF")
        future.add_done_callback(a)

    @tornado.gen.coroutine
    def dispatch(self):
        try:
            while True:
                msg = yield self.read_until(b"\x00\xFF")

                if self._read_listener:
                    self._read_listener(self, msg)

        except tornado.iostream.StreamClosedError as e:
            print(e)
        return

    @tornado.gen.coroutine
    def read_until(self, delimiter, _idalloc=itertools.count()):
        cb_id = next(_idalloc)
        cb = yield tornado.gen.Callback(cb_id)
        self.stream.read_until(delimiter, cb)
        result = yield tornado.gen.Wait(cb_id)
        raise tornado.gen.Return(result)

    _connect_listener = None
    def setConnectListener(self, fn):
        self._connect_listener = fn

    _read_listener = None
    def setReadListener(self, fn):
        self._read_listener = fn

    _close_listener = None
    def setCloseListener(self, fn):
        self._close_listener = fn
