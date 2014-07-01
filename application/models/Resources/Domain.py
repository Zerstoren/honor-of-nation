import models.Abstract.Domain
from .Mapper import Resources_Mapper

import models.User.Factory
import models.User.Domain


class Resources_Domain(models.Abstract.Domain.Abstract_Domain):
    def getUser(self):
        return models.User.Factory.User_Factory.getDomainById(
            self._domain_data['user']
        )

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self._domain_data['user'] = user.getId()
        else:
            self._domain_data['user'] = user

    def getMapper(self):
        return Resources_Mapper
