import models.Abstract.Mapper
from . import Common


class TownBonus_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'towns_bonus'

    def get(self, town):
        commonFilter = Common.Common_Filter()
        commonFilter.add('town', town.getId())

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()

        return self._select(commonFilter, commonLimit)

    def save(self, domain):
        commonSet = Common.Common_Set()
        commonSet\
            .add('town', domain.getTown().getId())\
            .add('eat', domain.getEat())\
            .add('minerals', domain.getMinerals())\
            .add('tax', domain.getTax())\
            .add('builds_speed', domain.getBuildsSpeed())\
            .add('riot', domain.getRiot())\
            .add('villagers', domain.getVillagers())\
            .add('max_villagers', domain.getMaxVillagers())\
            .add('armory_speed', domain.getArmorySpeed())\
            .add('armory_price', domain.getArmoryPrice())\
            .add('weapon_speed', domain.getWeaponSpeed())\
            .add('weapon_price', domain.getWeaponPrice())\
            .add('soliders_speed', domain.getSolidersSpeed())\
            .add('city_defence', domain.getCityDefence())\
            .add('city_steps', domain.getCitySteps())

        if domain.hasId():
            filterQuery = Common.Common_Filter()
            filterQuery.setId(domain.getId())
            self._update(commonSet, filterQuery)
        else:
            domain.setId(
                self._insert(commonSet)
            )

TownBonus_Mapper = TownBonus_Mapper_Main()
