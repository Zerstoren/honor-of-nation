import abc
import copy
import re

class Abstract_Domain(object, metaclass=abc.ABCMeta):
    def __init__(self, loaded=False):
        self._isLoaded = False
        self._domain_data = {}
        self._loaded = loaded

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
        return '_id' in self._domain_data

    def setOptions(self, options):
        if '_id' in options:
            self.setId(options['_id'])
            del options['_id']

        self.extract()

        for i in options:
            name = self.__convert(i)
            self.set(name, options[i])

    def extract(self, force=False):
        if not self.hasId():
            return self

        if not self._loaded or force:
            self._loaded = True

            self.setOptions(
                self.getMapper().getById(self.getId())
            )

        return self

    def toDict(self):
        result = copy.deepcopy(self._domain_data)
        if '_id' in result:
                result['_id'] = str(result['_id'])

        if 'remove' in result:
            del result['remove']

        return result

    def get(self, name):
        self.extract()
        return self._domain_data[name]

    def set(self, name, value):
        self.extract()
        self._domain_data[name] = value

    def has(self, name):
        return name in self._domain_data

    def _getFunc(self, name):
        name = self.__convert(name)
        def getFunc():
            self.extract()

            return self._domain_data[name]

        return getFunc

    def _setFunc(self, name):
        name = self.__convert(name)
        def setFunc(value):
            self.extract()

            self._domain_data[name] = value
            return self

        return setFunc

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
