import models.Abstract.Mapper
from . import Common


class TownResources_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'towns_resources'

    def get(self, town):
        commonFilter = Common.Common_Filter()
        commonFilter.add('town', town.getId())

        filterLimit = Common.Common_Limit()
        filterLimit.setOne()

        return self._select(commonFilter, filterLimit)

    def save(self, domain):
        commonSet = Common.Common_Set()
        commonSet\
            .add('town', domain.getTown().getId())\
            .add('tax', int(domain.getTax()))\
            .add('rubins', int(domain.getRubins()))\
            .add('wood', int(domain.getWood()))\
            .add('steel', int(domain.getSteel()))\
            .add('stone', int(domain.getStone()))\
            .add('eat', int(domain.getEat()))

        if domain.hasId():
            filterQuery = Common.Common_Filter()
            filterQuery.setId(domain.getId())
            self._update(commonSet, filterQuery)
        else:
            domain.setId(
                self._insert(commonSet)
            )


TownResources_Mapper = TownResources_Mapper_Main()
