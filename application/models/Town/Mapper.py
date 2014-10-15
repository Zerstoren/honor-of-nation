from models.Abstract.Common import Common_Set
import models.Abstract.Mapper
from . import Common

import exceptions.map

import models.Map.Common

class Town_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'towns'

    def getByPosition(self, mapCoordinate):
        commonFilter = Common.Common_Filter()
        commonFilter.add('pos_id', mapCoordinate.getPosId())

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()

        return self._select(commonFilter, commonLimit)

    def save(self, domain):
        """
        :type domain: models.Town.Domain.Town_Domain
        """
        assert(domain.getType() in [
            Common.VILLAGE,
            Common.CITY,
            Common.CASTLE
        ]);

        mapDomain = domain.getMap()

        if mapDomain.isBusyByBuild() and domain.getPosId() == mapDomain.getPosId() and not domain.hasId():
            raise exceptions.map.PositionIsBusy('Позиция уже занята')

        mapDomain.setBuildType(models.Map.Common.BUILD_TOWNS)
        mapDomain.getMapper().save(mapDomain)

        commonSet = Common.Common_Set()
        commonSet.add('pos_id', domain.getPosId())
        commonSet.add('type', domain.getType())
        commonSet.add('user', domain.getUser().getId())
        commonSet.add('population', domain.getPopulation())
        commonSet.add('name', domain.getName())

        if domain.hasId():
            self._update(
                commonSet,
                Common.Common_Filter({'_id', domain.getId()})
            )
        else:
            cursor = self._insert(commonSet)
            domain.setId(cursor)

Town_Mapper = Town_Mapper_Main()
