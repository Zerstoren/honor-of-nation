import models.Abstract.Factory

from . import Domain
from . import Mapper

class Resources_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getResources(self, userDomain):
        """
        :type userDomain: models.User.Domain.User_Domain
        """
        domain = Domain.Resources_Domain()
        domain.setOptions(
            Mapper.Resources_Mapper.getByUser(userDomain)
        )

        return domain

    def getDomainFromData(self, data):
        domain = Domain.Resources_Domain()
        domain.setOptions(data)

        return domain

Resources_Factory = Resources_Factory_Main()
