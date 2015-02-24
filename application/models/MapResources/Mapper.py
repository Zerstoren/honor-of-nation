import models.Abstract.Mapper
from . import Common

import models.Resources.Common
import models.Map.Common

import exceptions.database
import exceptions.message

class MapResources_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map_resources'

    def getResourceByPosition(self, mapCoordinate):
        commonFilter = Common.Common_Filter()
        commonFilter.add('pos_id', mapCoordinate.getPosId())

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()
        return self._select(commonFilter, commonLimit)

    def getResourceByTown(self, town):
        commonFilter = Common.Common_Filter()
        commonFilter.add('town', town.getId())

        return self._select(commonFilter)

    def getAll(self):
        return self._select()

    def save(self, domain):
        assert(domain.getType() in [
            models.Resources.Common.RUBINS,
            models.Resources.Common.STEEL,
            models.Resources.Common.STONE,
            models.Resources.Common.WOOD,
            models.Resources.Common.EAT,
        ])

        mapDomain = domain.getMap()

        if mapDomain.isBusyByBuild() and domain.getPosId() == mapDomain.getId() and not domain.hasId():
            raise exceptions.message.Message('Позиция уже занята')

        commonSet = Common.Common_Set()
        commonSet.add('pos_id', domain.getPosId())
        commonSet.add('type', domain.getType())
        commonSet.add('user', domain.getUser().getId() if domain.getUser() else None)
        commonSet.add('town', domain.getTown().getId() if domain.getTown() else None)
        commonSet.add('amount', domain.getAmount())
        commonSet.add('base_output', domain.getBaseOutput())
        commonSet.add('output', domain.getOutput())

        mapDomain.setBuild(models.Map.Common.BUILD_RESOURCES)
        mapDomain.getMapper().save(mapDomain)

        if domain.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id': domain.getId()})
            )
        else:
            cursor = self._insert(commonSet)
            domain.setId(cursor)


MapResources_Mapper = MapResources_Mapper_Main()
