import models.Abstract.Domain
from .Mapper import MapResources_Mapper

import models.User.Factory
import models.Map.Factory
import models.Town.Factory

import helpers.MapCoordinate

class MapResources_Domain(models.Abstract.Domain.Abstract_Domain):
    def getUser(self):
        userId = self._getFunc('user')()

        if userId:
            return models.User.Factory.User_Factory.getDomainById(userId)
        else:
            return None

    def getTown(self):
        townId = self._getFunc('town')()

        if townId:
            return models.Town.Factory.Town_Factory.getDomainById(townId)

    def getMap(self):
        return models.Map.Factory.Map_Factory.getDomainById(
            helpers.MapCoordinate.MapCoordinate(posId=self.getPosId()).getPosId()
        )

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return MapResources_Mapper
