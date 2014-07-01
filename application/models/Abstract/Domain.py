import abc
import copy

class Abstract_Domain(object, metaclass=abc.ABCMeta):
    def __init__(self):
        self._isLoaded = False
        self._domain_data = {}

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
        def getFunc():
            self._loadData()

            return self._domain_data[name]

        return getFunc

    def _setFunc(self, name):
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
                return self._getFunc(item.replace('get', '').lower())

        elif item[0:3] == 'set':
            try:
                return super().__getattribute__(item)
            except AttributeError:
                return self._setFunc(item.replace('set', '').lower())

        else:
            return super().__getattribute__(item)
