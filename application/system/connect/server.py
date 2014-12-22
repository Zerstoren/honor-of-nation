import itertools
import socket

import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver

SOCKET_END = b"\r\n\r\n"

class SimpleEcho(object):
    """
        Per-connection object.
    """
    stream = None
    @tornado.gen.coroutine
    def on_disconnect(self):
        if self._close_listener:
            self._close_listener(self)

        yield []
        return

    @tornado.gen.coroutine
    def dispatch(self):
        try:
            while True:
                msg = yield self.read_until(SOCKET_END)

                if self._read_listener:
                    self._read_listener(self, msg)
        except tornado.iostream.StreamClosedError:
            pass
        return

    @tornado.gen.coroutine
    def read_until(self, delimiter, _idalloc=itertools.count()):
        cb_id = next(_idalloc)
        cb = yield tornado.gen.Callback(cb_id)
        self.stream.read_until(delimiter, cb, 65000)
        result = yield tornado.gen.Wait(cb_id)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def write(self, data):
        yield tornado.gen.Task(self.stream.write, data + SOCKET_END)

    @tornado.gen.coroutine
    def on_connect(self):
        yield self.dispatch()
        return

    _read_listener = None
    def setReadListener(self, fn):
        self._read_listener = fn

    _close_listener = None
    def setCloseListener(self, fn):
        self._close_listener = fn

    def setStream(self, stream):
        """
        :type stream: tornado.iostream.IOStream
        """
        self.stream = stream


class SimpleEchoServer(tornado.tcpserver.TCPServer):
    """
        Server listener object.
    """
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        conn = SimpleEcho()

        stream.set_close_callback(conn.on_disconnect)
        stream.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        stream.socket.setsockopt(socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)

        conn.setStream(stream)

        if self._connect_listener:
            self._connect_listener(conn)

        yield conn.on_connect()

        return

    _connect_listener = None
    def setConnectListener(self, fn):
        self._connect_listener = fn

class BalancerBroker():

    def __init__(self, address='127.0.0.1', port=8888):
        self.connections = []
        self.messages_queue = []
        self.sendMsgId = itertools.count()

        self.tcp = SimpleEchoServer()
        self.tcp.listen(port=port, address=address)
        self.tcp.setConnectListener(self.onConnectNewClient)

    def onConnectNewClient(self, connector):
        if len(self.connections) == 0:
            import balancer.server.clientConnector
            balancer.server.clientConnector.ClientPool.sendStartup()

        connector.setReadListener(self.onMessage)
        connector.setCloseListener(self.onConnectClose)
        self.connections.append(connector)

        if len(self.messages_queue):
            for i in self.messages_queue:
                self.write(i)

            self.messages_queue = []

    def write(self, data):
        if len(self.connections) == 0:
            self.messages_queue.append(data)
            return

        sendTo = next(self.sendMsgId)
        self.connections[sendTo % len(self.connections)].write(data)

    def onMessage(self, connector, data):
        pass

    def isReady(self):
        return len(self.connections) != 0

    def onConnectClose(self, connector):
        self.connections.remove(connector)

        if len(self.connections) == 0:
            import balancer.server.clientConnector
            balancer.server.clientConnector.ClientPool.sendDropDown()
