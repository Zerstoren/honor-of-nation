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
        userId = self.get('user')
        return models.User.Factory.User_Factory.getDomainById(userId)

    def setUser(self, user):
        if isinstance(user, models.User.Domain.User_Domain):
            self.set('user', user.getId())
        else:
            self.set('user', user)

    def getArmor(self):
        """
        :rtype: models.Equipment.Armor.Domain.Equipment_Armor_Domain
        """
        if self.armor is None:
            self.armor = service.Equipment.Armor.Service_Equipment_Armor().getForce(
                self.get('armor')
            )

        return self.armor

    def setArmor(self, armor):
        self.armor = None

        if isinstance(armor, Equipment_Armor_Domain):
            self.set('armor', armor.getId())
        else:
            self.set('armor', armor)

    def getWeapon(self):
        """
        :rtype: models.Equipment.Weapon.Domain.Equipment_Weapon_Domain
        """
        if self.weapon is None:
            self.weapon = service.Equipment.Weapon.Service_Equipment_Weapon().getForce(
                self.get('weapon')
            )

        return self.weapon

    def setWeapon(self, weapon):
        self.weapon = None

        if isinstance(weapon, Equipment_Weapon_Domain):
            self.set('weapon', weapon.getId())
        else:
            self.set('weapon', weapon)

    def getWeaponSecond(self):
        """
        :rtype: models.Equipment.Weapon.Domain.Equipment_Weapon_Domain
        """
        if self.weaponSecond is None:
            result = self.get('weapon_second')

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
            self.set('weapon_second', weapon.getId())
        else:
            self.set('weapon_second', weapon)

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