import models.Abstract.Mapper
from . import Common
import models.Resources.Common

import exceptions.database

class MapResources_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map_resources'

    def getResourceByPosition(self, mapCoordinate):
        commonFilter = Common.Common_Filter()
        commonFilter.add('pos_id', mapCoordinate.getPosId())

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()

        return self._select(commonFilter, commonLimit)

    def save(self, domain):
        assert(domain.getType() in [
            models.Resources.Common.RUBINS,
            models.Resources.Common.STEEL,
            models.Resources.Common.STONE,
            models.Resources.Common.WOOD,
            models.Resources.Common.EAT,
        ])

        commonSet = Common.Common_Set()
        commonSet.add('pos_id', domain.getPosId())
        commonSet.add('type', domain.getType())
        commonSet.add('user', domain.getUser().getId() if domain.getUser() else None)
        commonSet.add('town', domain.getTown().getId() if domain.getTown() else None)
        commonSet.add('amount', domain.getAmount())
        commonSet.add('base_output', domain.getBaseOutput()),
        commonSet.add('output', domain.getOutput()),

        if domain.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id': domain.getId()})
            )
        else:
            cursor = self._insert(commonSet)
            domain.setId(cursor)

MapResources_Mapper = MapResources_Mapper_Main()
