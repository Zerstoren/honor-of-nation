import models.Abstract.Mapper
from . import Common
import exceptions.database

class Map_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map'

    def getByPositionId(self, posId):
        queryFilter = Common.Common_Filter()
        queryFilter.add('pos_id', int(posId))

        queryLimit = Common.Common_Limit()
        queryLimit.setOne()

        result = self._select(queryFilter, queryLimit)
        if result is None:
            raise exceptions.database.NotFound('Map item by position id %s not found' % posId)

        return result

    def getByChunks(self, chunks):
        queryFilter = Common.Common_Filter()
        queryFilter.addIn('chunk', chunks)

        return self._select(queryFilter)

    def getByPosIds(self, posIds):
        queryFilter = Common.Common_Filter()
        queryFilter.addIn('pos_id', posIds)

        return self._select(queryFilter)

    def getRegion(self, regionMap):
        """
        :type regionMap: helpers.MapRegion.MapRegion
        """
        queryFilter = Common.Common_Filter()
        queryFilter.add('x', {'$gte': regionMap.getFromX(), '$lte': regionMap.getToX()})
        queryFilter.add('y', {'$gte': regionMap.getFromY(), '$lte': regionMap.getToY()})

        return self._select(queryFilter)

    def save(self, domain):
        """
        :type domain: models.Map.Domain.Map_Domain
        """
        data = Common.Common_Set()
        data.fromDomain(domain)

        if domain.hasId():
            filterData = Common.Common_Filter({
                '_id': domain.getId()
            })
            self._update(data, filterData)
        else:
            self._insert(data)


Map_Mapper = Map_Mapper_Main()
