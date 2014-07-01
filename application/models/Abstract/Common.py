import system.mongo

class Common_Set(dict):
    def __init__(self, options=None):
        super().__init__()

        options = options if options is not None else {}

        if options:
            for i in options:
                self.add(i, options[i])

    def add(self, option, value):
        self[option] = value
        return self


class Common_Filter(Common_Set):
    def __init__(self, options=None):
        super().__init__(options if options else {})
        self['remove'] = 0

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
