from models.User.Domain import User_Domain
from exceptions.httpCodes import Page401

import json
from tornado import websocket


class UserNotSet(Page401):
    pass


class UserTransfer(object):
    socket = None
    _user = None
    async = None

    def connect(self, socket):
        assert isinstance(socket, websocket.WebSocketHandler)
        self.socket = socket
        self.collect = False
        self.pool = []

    def disconnect(self):
        self.rmUser()
        self.socket = None

    def setAsync(self, async):
        """
        :type async: bool
        """
        self.async = async

    def rmAsync(self):
        self.async = None

    def startCollect(self):
        self.collect = True

    def purge(self):
        self.socket.write_message(json.dumps({
            'collection': self.pool
        }))

        self.collect = False
        self.pool = []

    def send(self, module, message):
        """
        :type module: string
        :type message: dict
        """
        assert type(message) == dict
        assert type(module) == str

        sendData = {
            "message": message,
            "module": module,
            "async": self.async
        }

        self.rmAsync()

        if self.collect is False:
            self.socket.write_message(json.dumps(sendData))
        else:
            self.pool.append(sendData)

    def hasUser(self):
        return self._user is not None

    def getUser(self):
        if self._user is None:
            raise UserNotSet('User not set')

        return self._user

    def setUser(self, userDomain):
        """
        :type userDomain: models.User.Domain.User_Domain
        """
        assert isinstance(userDomain, User_Domain)

        self._user = userDomain
        userDomain._setTransfer(self)

    def rmUser(self):
        self._user._removeTransfer()
        self._user = None
