import config
import system.connect.server

import balancer.server.userPool

import pickle


class Receiver_Instance():
    def __init__(self, address='127.0.0.1', port=8888):
        self.connections = []
        self.messages_queue = []

        self.tcp = system.connect.server.SimpleEchoServer()
        self.tcp.listen(port=port, address=address)
        self.tcp.setConnectListener(self.onConnectNewClient)

    def onConnectNewClient(self, connector):
        print("Connected new celery")
        connector.setReadListener(self.onMessage)
        connector.setCloseListener(self.onConnectClose)
        self.connections.append(connector)


    def write(self, data):
        raise DeprecationWarning('Receiver not support message send')

    def onMessage(self, connector, data):
        try:
            info = pickle.loads(data)
            print("Balancer", info)

            connector = balancer.server.userPool.UserPool.getUser(info['user'])
            connector.send(info['data'])

        except KeyError:
            pass

    def onConnectClose(self, connector):
        self.connections.remove(connector)


Receiver = Receiver_Instance(
    config.get('balancer.celery.server.host'),
    int(config.get('balancer.celery.server.port'))
)
