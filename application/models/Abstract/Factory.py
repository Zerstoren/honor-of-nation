
class Abstract_Factory(object):
    __cache = None

    def __init__(self):
        self.__cache = {}

    def setCache(self, domainId, domain):
        if domainId in self.__cache:
            raise Exception("Domain already in cache")

        self.__cache[domainId] = domain

    def getCache(self, domainId):
        return self.__cache[domainId] if domainId in self.__cache else None

    def _cleanIndexes(self):
        self.__cache = []