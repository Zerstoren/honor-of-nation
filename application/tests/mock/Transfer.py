#!/usr/bin/env python
# -*- coding: utf-8 -*-

from system.UserTransfer import UserTransfer
from models.User import Domain


class TransferMock(UserTransfer):
    def __init__(self, user):
        assert isinstance(user, Domain.User_Domain)

        user._setTransfer(self)

        self._user = user
        self.__lastMessage = []

    def send(self, module, message):
        assert type(message) == dict
        assert type(module) == str

        sendData = {
            "message": message,
            "module": module,
            "async": self.async
        }

        self.__lastMessage.append(sendData)

    def getLastMessage(self, n=0):
        return self.__lastMessage[len(self.__lastMessage) - 1 - n]

