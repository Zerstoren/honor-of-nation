import models.Abstract.Domain
from .Mapper import Equipment_Armor_Mapper

import models.User.Factory
import models.User.Domain


class Equipment_Armor_Domain(models.Abstract.Domain.Abstract_Domain):
    def getShield(self):
        return True if self.has('shield') and self.get('shield') else False

    def getShieldType(self):
        if self.getShield():
            return self.get('shield_type')
        else:
            return False

    def getShieldBlocking(self):
        if self.getShield():
            return self.get('shield_blocking')
        else:
            return False

    def getShieldDurability(self):
        if self.getShield():
            return self.get('shield_durability')
        else:
            return False

    def getUser(self):
        userId = self.get('user')
        return models.User.Factory.User_Factory.getDomainById(userId)

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self.set('user', user.getId())
        else:
            self.set('user', user)

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return Equipment_Armor_Mapper

    def extract(self, force=False):
        if not self.hasId():
            return self

        if not self._loaded or force:
            self._loaded = True

            self.setOptions(
                self.getMapper().getById(self.getId(), force=True)
            )

        return self