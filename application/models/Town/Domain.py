import models.Abstract.Domain

import service.User

from .Mapper import Town_Mapper

import helpers.MapCoordinate

import models.Map.Factory
import models.User.Domain

class MapResources_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMap(self):
        return models.Map.Factory.Map_Factory.getDomainByPosition(
            helpers.MapCoordinate.MapCoordinate(posId=self.getPosId())
        )

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return Town_Mapper

    def setUser(self, obj):
        if isinstance(obj, models.User.Domain.User_Domain):
            self._domain_data['user'] = obj
        else:
            self._domain_data['user'] = service.User.Service_User().getUserDomain(obj)