import models.Abstract.Mapper
from . import Common

import models.Resources.Common


class Equipment_Weapon_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'equipment_weapon'

    def save(self, weapon):
        """
        :type domain: models.Equipment.Weapon.Domain.Equipment_Weapon_Domain
        """

        commonSet = Common.Common_Set()
        commonSet.add('type', weapon.getType())
        commonSet.add('user', weapon.getUser().getId())

        commonSet.add('damage', weapon.getDamage())
        commonSet.add('speed', weapon.getSpeed())
        commonSet.add('critical_chance', weapon.getCriticalChance())
        commonSet.add('critical_damage', float(weapon.getCriticalDamage()))

        commonSet.add('level', weapon.getLevel())
        commonSet.add('time', weapon.getTime())

        commonSet.add(models.Resources.Common.RUBINS, weapon.getRubins())
        commonSet.add(models.Resources.Common.WOOD, weapon.getWood())
        commonSet.add(models.Resources.Common.STEEL, weapon.getSteel())
        commonSet.add(models.Resources.Common.EAT, weapon.getEat())

        if weapon.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id', weapon.getId()})
            )
        else:
            weaponId = self._insert(commonSet)
            weapon.setId(weaponId)

    def getByUser(self, user):
        commonFilter = Common.Common_Filter()
        commonFilter.add('user', user.getId())

        return self._select(commonFilter)

Equipment_Weapon_Mapper = Equipment_Weapon_Mapper_Main()
