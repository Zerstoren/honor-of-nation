import models.Abstract.Mapper
from . import Common

import models.Resources.Common


class Equipment_Armor_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'equipment_armor'

    def save(self, armor):
        """
        :type domain: models.Equipment.Armor.Domain.Equipment_Armor_Domain
        """

        commonSet = Common.Common_Set()
        commonSet.add('type', armor.getType())
        commonSet.add('user', armor.getUser().getId())

        commonSet.add('health', armor.getHealth())
        commonSet.add('agility', armor.getAgility())
        commonSet.add('absorption', armor.getAbsorption())

        commonSet.add('shield', armor.getShield())
        commonSet.add('shield_type', armor.getShieldType())
        commonSet.add('shield_blocking', armor.getShieldBlocking())
        commonSet.add('shield_durability', armor.getShieldDurability())

        # commonSet.add('horse', armor.getHorse())
        # commonSet.add('horse_health', armor.getHorseHealth())
        # commonSet.add('horse_slope', armor.getHorseSlope())

        commonSet.add('level', armor.getLevel())
        commonSet.add('time', armor.getTime())

        commonSet.add(models.Resources.Common.RUBINS, armor.getRubins())
        commonSet.add(models.Resources.Common.WOOD, armor.getWood())
        commonSet.add(models.Resources.Common.STEEL, armor.getSteel())
        commonSet.add(models.Resources.Common.EAT, armor.getEat())

        if armor.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id', armor.getId()})
            )
        else:
            armorId = self._insert(commonSet)
            armor.setId(armorId)

    def getByUser(self, user):
        commonFilter = Common.Common_Filter()
        commonFilter.add('user', user.getId())

        return self._select(commonFilter)

Equipment_Armor_Mapper = Equipment_Armor_Mapper_Main()
