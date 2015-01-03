import models.Abstract.Mapper
from . import Common

import models.Resources.Common

import exceptions.database


class Equipment_Units_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'equipment_units'

    def getById(self, queryId, force=False):
        commonFilter = Common.Common_Filter()
        commonFilter.setId(queryId)

        if force:
            commonFilter.rm('remove')

        result = self._select(
            Common.Common_Filter().setId(queryId),
            Common.Common_Limit().setOne()
        )

        if result is None:
            raise exceptions.database.NotFound('Data by _id %s not found in table `%s`' % (queryId, self._table))

        return result

    def save(self, unit):
        """
        :type unit: models.Equipment.Units.Domain.Equipment_Units_Domain
        """
        commonSet = Common.Common_Set()
        commonSet.add('type', unit.getType())
        commonSet.add('user', unit.getUser().getId())

        if unit.getType() == Common.TYPE_GENERAL:
            commonSet.add('troop_size', unit.getTroopSize())
        else:
            commonSet.add('troop_size', 0)

        commonSet.add('health', unit.getHealth())
        commonSet.add('strength', unit.getStrength())
        commonSet.add('agility', unit.getAgility())
        commonSet.add('absorption', unit.getAbsorption())
        commonSet.add('stamina', unit.getStamina())

        commonSet.add('armor', unit.getArmor().getId())
        commonSet.add('weapon', unit.getWeapon().getId())

        if unit.getWeaponSecond():
            commonSet.add('weapon_second', unit.getWeaponSecond().getId())
        else:
            commonSet.add('weapon_second', False)

        commonSet.add('time', unit.getTime())

        commonSet.add(models.Resources.Common.RUBINS, unit.getRubins())
        commonSet.add(models.Resources.Common.WOOD, unit.getWood())
        commonSet.add(models.Resources.Common.STEEL, unit.getSteel())
        commonSet.add(models.Resources.Common.EAT, unit.getEat())

        if unit.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id', unit.getId()})
            )
        else:
            unitId = self._insert(commonSet)
            unit.setId(unitId)

    def getByUser(self, user):
        commonFilter = Common.Common_Filter()
        commonFilter.add('user', user.getId())

        return self._select(commonFilter)

Equipment_Units_Mapper = Equipment_Units_Mapper_Main()
