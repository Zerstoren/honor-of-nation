import models.abstract.Domain
import models.abstract.Writer

import copy

factory = None
mapper = None


class MockDomain(models.abstract.Domain.Domain):
    def __init__(self):
        self._mapper = mapper
        self._factory = factory
        self.__data = {}
        self.__domainExtend = {}

    def getId(self):
        return self.__data['_id']

    def getA(self):
        return self.__data['a']

    def getB(self):
        return self.__data['b']

    def getC(self):
        return self.__data['c']

    def _getData(self, clone=False):
        return copy.copy(self.__data) if clone else self.__data

    def _setData(self, newData):
        self.__data = self._merge(self.__data, newData)

    def edit(self):
        return self._getLock(Writer(self))


class Writer(models.abstract.Writer.Writer):
    def __init__(self, writed):
        super().__init__()
        self._writed = writed
        self._mapper = mapper
        self._factory = factory
        self._transaction = writed._getData(True)

    def setA(self, a):
        self._transaction['a'] = a

    def setB(self, b):
        self._transaction['b'] = b

    def setC(self, c):
        assert type(c) == int
        self._transaction['c'] = c

    def getId(self):
        return self._transaction['_id']

    def setId(self, itemId):
        if '_id' not in self._transaction:
            self._transaction['_id'] = itemId

    def onTransaction(self):
        self._writed._setData(self._transaction)
        self._transaction = {}
        return self
