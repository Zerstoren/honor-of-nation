import models.Abstract.Mapper
from . import Common
import models.Map.Math
import models.Resources.Common

import exceptions.database

class MapResources_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map_resources'

    def getResourceByPosition(self, x, y):
        commonFilter = Common.Common_Filter()
        commonFilter.add('pos_id', models.Map.Math.fromPositionToId(x, y))

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()

        try:
            return self._select(commonFilter, commonLimit)
        except exceptions.database.NotFound:
            return False


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
        commonSet.add('user', domain.getUser())
        commonSet.add('town', domain.getTown())
        commonSet.add('count', domain.getCount())
        commonSet.add('production', domain.getProduction())

        if domain.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id': domain.getId()})
            )
        else:
            cursor = self._insert(commonSet)
            domain.setId(cursor)

MapResources_Mapper = MapResources_Mapper_Main()
