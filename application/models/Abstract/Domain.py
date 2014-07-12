import abc
import copy
import re

class Abstract_Domain(object, metaclass=abc.ABCMeta):
    def __init__(self):
        self._isLoaded = False
        self._domain_data = {}

    def __convert(self, name):
        return re.sub('(?!^)([A-Z]+)', r'_\1',name).lower()

    @abc.abstractmethod
    def getMapper(self):
        pass

    def setId(self, queryId):
        self._domain_data['_id'] = queryId

    def getId(self):
        return self._domain_data['_id']

    def hasId(self):
        return 'id' in self._domain_data

    def setOptions(self, options):
        for i in options:
            self.__getattribute__('set' + i)(options[i])

    def _getFunc(self, name):
        name = self.__convert(name)
        def getFunc():
            self._loadData()

            return self._domain_data[name]

        return getFunc

    def _setFunc(self, name):
        name = self.__convert(name)
        def setFunc(value):
            self._loadData()

            self._domain_data[name] = value
            return self

        return setFunc

    def _loadData(self):
        if 'id' in self._domain_data and self._isLoaded == False:
            self._isLoaded = True
            cursor = self.getMapper().getById(self._domain_data['_id'])

            self.setOptions(cursor)

    def __getattribute__(self, item):
        """
        :type item: str
        """

        if item[0:3] == 'get':
            try:
                return super().__getattribute__(item)
            except AttributeError:
                return self._getFunc(item.replace('get', ''))

        elif item[0:3] == 'set':
            try:
                return super().__getattribute__(item)
            except AttributeError:
                return self._setFunc(item.replace('set', ''))

        else:
            return super().__getattribute__(item)
