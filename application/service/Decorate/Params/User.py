import helpers.mongo

class Decorate():
    def getUserDomain(self, domainId):
        return super().getUserDomain(
            helpers.mongo.objectId(domainId)
        )