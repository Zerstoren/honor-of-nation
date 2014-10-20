import models.Abstract.Domain
from .Mapper import Resources_Mapper

import models.User.Factory
import models.User.Domain


class Resources_Domain(models.Abstract.Domain.Abstract_Domain):
    def getUser(self):
        return models.User.Factory.User_Factory.getDomainById(
            self._getFunc('user')()
        )

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self._setFunc('user')(user.getId())
        else:
            self._setFunc('user')(user)

    def getMapper(self):
        return Resources_Mapper

    def toDict(self):
        result = super().toDict()

        del result['user']
        del result['_id']

        return result