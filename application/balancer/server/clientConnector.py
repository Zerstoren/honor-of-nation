import uuid

from tornado import websocket

import balancer.server.userPool


class ClientConnector():
    userId = None
    _id = None

    def connect(self, socket):
        assert isinstance(socket, websocket.WebSocketHandler)
        self.socket = socket
        self._id = str(uuid.uuid4())

        ClientPool.add(self)

    def disconnect(self):
        self.socket = None
        self.rmUser()
        ClientPool.remove(self)

    def getSocketId(self):
        return self._id

    def send(self, data):
        self.socket.write_message(data)

    def getUser(self):
        return self.userId

    def setUser(self, userId):
        self.userId = userId
        balancer.server.userPool.UserPool.addUser(self, userId)

    def rmUser(self):
        if self.userId:
            balancer.server.userPool.UserPool.removeUser(self.userId)


class ClientPool_Instance():
    clients = {}

    def get(self, socketId):
        return self.clients[socketId]

    def add(self, connected):
        self.clients[connected.getSocketId()] = connected

    def remove(self, connected):
        del self.clients[connected.getSocketId()]


ClientPool = ClientPool_Instance()
