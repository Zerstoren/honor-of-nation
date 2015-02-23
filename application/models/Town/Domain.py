import models.Abstract.Domain

from .Mapper import Town_Mapper

import helpers.MapCoordinate

import models.Map.Factory
import models.User.Domain
import models.User.Factory
import models.TownBuilds.Factory
import models.TownResources.Factory
import models.TownBonus.Factory

class Town_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMap(self):
        return models.Map.Factory.Map_Factory.getDomainById(
            helpers.MapCoordinate.MapCoordinate(posId=self.getPosId()).getPosId()
        )

    def getUser(self):
        userId = self.get('user')
        return models.User.Factory.User_Factory.getDomainById(userId)

    def getBuilds(self):
        """
        :rtype: models.TownBuilds.Domain.TownBuilds_Domain
        """
        return models.TownBuilds.Factory.TownBuilds_Factory.getByTown(self)

    def getResourcesUp(self):
        return models.TownResources.Factory.TownResources_Factory.get(self)

    def getBonus(self):
        return models.TownBonus.Factory.TownBonus_Factory.get(self)

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return Town_Mapper

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self.set('user', user.getId())
        else:
            self.set('user', user)