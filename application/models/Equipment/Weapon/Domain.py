import models.Abstract.Domain
from .Mapper import Equipment_Weapon_Mapper

import models.User.Factory
import models.User.Domain


class Equipment_Weapon_Domain(models.Abstract.Domain.Abstract_Domain):

    def getUser(self):
        userId = self._getFunc('user')()
        return models.User.Factory.User_Factory.getDomainById(userId)

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self._domain_data['user'] = user.getId()
        else:
            self._domain_data['user'] = user

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return Equipment_Weapon_Mapper

    def extract(self, force=False):
        if not self.hasId():
            return self

        if not self._loaded or force:
            self._loaded = True

            self.setOptions(
                self.getMapper().getById(self.getId(), force=True)
            )

        return self