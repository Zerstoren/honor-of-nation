import config
import system.connect.server
import system.log

import network.server.userPool

import pickle


class Receiver_Instance():
    def __init__(self, address='127.0.0.1', port=8888):
        self.connections = []
        self.messages_queue = []
        self._onMessage = None

        self.tcp = system.connect.server.SimpleEchoServer()
        self.tcp.listen(port=port, address=address)
        self.tcp.setConnectListener(self.onConnectNewClient)

    def onConnectNewClient(self, connector):
        connector.setReadListener(self.onMessage)
        connector.setCloseListener(self.onConnectClose)
        self.connections.append(connector)

    def write(self, data):
        raise DeprecationWarning('Receiver not support message send')

    def onMessage(self, connector, data):
        info = pickle.loads(data)
        self._onMessage(info)

    def onConnectClose(self, connector):
        self.connections.remove(connector)

    def setOnMessage(self, fn):
        self._onMessage = fn


Receiver = Receiver_Instance(
    config.get('battle.server.host'),
    int(config.get('battle.server.port'))
)
