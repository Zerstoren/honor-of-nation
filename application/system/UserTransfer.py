from models.User.Domain import User_Domain

from exceptions.httpCodes import Page401

import helpers.mongo

import json

import init_celery


class UserNotSet(Page401):
    pass


class UserTransfer(object):
    _user = None
    async = None

    def __init__(self):
        self.collect = False
        self.pool = []

    def disconnect(self):
        pass
        # self.rmUser()

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
        send = {'collection': self.pool}

        self.collect = False
        self.pool = []

        return send

    def send(self, module, message, urgent=False):
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

        if self.collect is False or urgent is True:
            init_celery.message(sendData, self.getUser())
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

    def setUserById(self, userId):
        domain = User_Domain()
        domain.setId(
            helpers.mongo.objectId(userId)
        )
        domain._setTransfer(self)

        self._user = domain

    def rmUser(self):
        self._user = None
