import system.mongo
from inspect import isfunction

class Common_Set(dict):
    require = []

    def __init__(self, options=None):
        super().__init__()

        options = options if options is not None else {}

        if options:
            for i in options:
                self.add(i, options[i])

    def add(self, option, value):
        self[option] = value
        return self

    def set(self, key, value):
        try:
            if isfunction(self.__getattribute__(key)) and (key not in ['add', 'fromDomain', 'test']):
                self.__getattribute__(key)(value)
            else:
                raise Exception(key + ' is not function for set data')
        except:
            self.add(key, value)

    def fromDomain(self, domain):
        """
        :type domain: models.Abstract.Domain.Abstract_Domain
        """
        for key in domain._domain_data:
            if key == '_id':
                continue

            self.set(key, domain._domain_data[key])

    def test(self, exception=True):
        if not len(self.require):
            return True
        keys = list(self.keys())
        for key in self.require:
            if key not in keys:
                if exception:
                    print(self)
                    raise Exception('Test ' + self.__class__.__name__ + ' is failed, key %s not exist' % key)
                else:
                    return False

        return True


class Common_Filter(dict):

    def __init__(self, options=None):
        if options and 'id' in options:
            raise Exception('In common filter you set id, need to use _id')

        super().__init__()

        if options:
            for i in options:
                self.add(i, options[i])

        self['remove'] = 0

    def add(self, option, value):
        self[option] = value
        return self

    def addIn(self, option, values):
        self[option] = {
            '$in': values
        }

    def setId(self, recordId):
        self.add('_id', system.mongo.mongo.id(recordId))
        return self

class Common_Limit(object):
    limit = None
    start = None
    complete = None

    def setOne(self):
        self.setLimit(1)
        return self

    def setLimit(self, limit):
        self.limit = limit
        return self

    def setRange(self, start, complete):
        self.start = start
        self.complete = complete
        return self

    def getLimit(self):
        if self.limit is not None:
            return [self.limit]
        elif self.start is not None and self.complete is not None:
            return [self.start, self.complete]
        else:
            return []

    def hasLimit(self):
        return bool(self.getLimit())

    def isOneRecord(self):
        return True if self.limit is not None and self.limit == 1 else False


class Common_Order(object):
    pass
