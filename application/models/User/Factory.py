import models.Abstract.Factory
from . import Domain
from . import Mapper

class User_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainById(self, userId):
        domain = self.getCache(userId)
        if domain is None:
            domain = self.getDomainFromData(
                Mapper.User_Mapper.getById(userId)
            )

        return domain

    def getDomainFromData(self, data):
        """
        :rtype: models.User.Domain.User_Domain
        """
        domain = self.getCache(data['_id'])

        if domain is None:
            domain = Domain.User_Domain()
            domain.setOptions(data)
            self.setCache(domain.getId(), domain)

        return domain

User_Factory = User_Factory_Main()
