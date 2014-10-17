import models.Abstract.Factory
import models.User.Domain
import models.User.Mapper
from collection import UserCollection

class User_Factory_Main(models.Abstract.Factory.Abstract_Factory):

    def getDomainById(self, userId):
        domain = self.getCache(userId)
        if domain is None:
            domain = models.User.Domain.User_Domain()
            domain.setId(userId)

            self.setCache(domain.getId(), domain)

        return domain

    def getCollectionFromDataNoCache(self, data):
        collection = UserCollection.User_Collection()

        for i in data:
            domain = models.User.Domain.User_Domain()
            domain.setOptions(i)
            collection.append(domain)

        return collection

    def getDomainFromData(self, data):
        """
        :rtype: models.User.Domain.User_Domain
        """
        domain = self.getCache(data['_id'])

        if domain is None:
            domain = models.User.Domain.User_Domain()
            domain.setOptions(data)
            self.setCache(domain.getId(), domain)

        return domain

User_Factory = User_Factory_Main()
