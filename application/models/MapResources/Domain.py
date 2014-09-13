import models.Abstract.Domain
from .Mapper import MapResources_Mapper

import models.User.Factory

class MapResources_Domain(models.Abstract.Domain.Abstract_Domain):
    def getUser(self):
        userId = self._getFunc('user')()

        if userId:
            return models.User.Factory.User_Factory.getDomainById(userId)
        else:
            return None

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return MapResources_Mapper
