import models.Abstract.Domain

import service.User

from .Mapper import Town_Mapper

import helpers.MapCoordinate

import models.Map.Factory
import models.User.Domain
import models.User.Factory

class Town_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMap(self):
        return models.Map.Factory.Map_Factory.getDomainById(
            helpers.MapCoordinate.MapCoordinate(posId=self.getPosId()).getPosId()
        )

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
        return Town_Mapper

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self._domain_data['user'] = user.getId()
        else:
            self._domain_data['user'] = user