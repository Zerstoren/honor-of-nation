import models.Abstract.Domain
from .Mapper import Equipment_Units_Mapper

import models.User.Factory
import models.User.Domain

# import models.Equipment.Armor.Factory
# import models.Equipment.Weapon.Factory

import service.Equipment.Armor
import service.Equipment.Weapon

from models.Equipment.Armor.Domain import Equipment_Armor_Domain
from models.Equipment.Weapon.Domain import Equipment_Weapon_Domain


class Equipment_Units_Domain(models.Abstract.Domain.Abstract_Domain):
    armor = None
    weapon = None
    weaponSecond = None

    def getUser(self):
        userId = self._getFunc('user')()
        return models.User.Factory.User_Factory.getDomainById(userId)

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self._domain_data['user'] = user.getId()
        else:
            self._domain_data['user'] = user

    def getArmor(self):
        """
        :rtype: models.Equipment.Armor.Domain.Equipment_Armor_Domain
        """
        if self.armor is None:
            self.armor = service.Equipment.Armor.Service_Equipment_Armor().getForce(
                self._domain_data['armor']
            )

        return self.armor

    def setArmor(self, armor):
        self.armor = None

        if isinstance(armor, Equipment_Armor_Domain):
            self._domain_data['armor'] = armor.getId()
        else:
            self._domain_data['armor'] = armor

    def getWeapon(self):
        """
        :rtype: models.Equipment.Weapon.Domain.Equipment_Weapon_Domain
        """
        if self.weapon is None:
            self.weapon = service.Equipment.Weapon.Service_Equipment_Weapon().getForce(
                self._domain_data['weapon']
            )

        return self.weapon

    def setWeapon(self, weapon):
        self.weapon = None

        if isinstance(weapon, Equipment_Weapon_Domain):
            self._domain_data['weapon'] = weapon.getId()
        else:
            self._domain_data['weapon'] = weapon

    def getWeaponSecond(self):
        """
        :rtype: models.Equipment.Weapon.Domain.Equipment_Weapon_Domain
        """
        if self.weaponSecond is None:
            result = self._domain_data['weapon_second']

            if result:
                self.weaponSecond = service.Equipment.Weapon.Service_Equipment_Weapon().getForce(
                    result
                )
            else:
                self.weaponSecond = False

        return self.weaponSecond

    def setWeaponSecond(self, weapon):
        self.weaponSecond = None

        if isinstance(weapon, Equipment_Weapon_Domain):
            self._domain_data['weapon_second'] = weapon.getId()
        else:
            self._domain_data['weapon_second'] = weapon

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return Equipment_Units_Mapper

    def extract(self, force=False):
        if not self.hasId():
            return self

        if not self._loaded or force:
            self._loaded = True

            self.setOptions(
                self.getMapper().getById(self.getId(), force=True)
            )

        return self