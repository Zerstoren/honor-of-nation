import models.Abstract.Mapper
from . import Common
import exceptions.database

class Map_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map'

    def getByPositionId(self, posId):
        queryFilter = Common.Common_Filter()
        queryFilter.add('_id', int(posId))

        queryLimit = Common.Common_Limit()
        queryLimit.setOne()

        result = self._select(queryFilter, queryLimit)
        if result is None:
            raise exceptions.database.NotFound('Map item by position id %s not found' % posId)

        result['map_status'] = 1
        return result

    def getByChunks(self, chunks):
        queryFilter = Common.Common_Filter()
        queryFilter.addIn('chunk', chunks)

        return self._select(queryFilter)

    def getByPosIds(self, posIds):
        queryFilter = Common.Common_Filter()
        queryFilter.addIn('_id', posIds)

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
        data.add('land', domain.getLand())
        data.add('land_type', domain.getLandType())
        data.add('x', domain.getX())
        data.add('y', domain.getY())
        data.add('build', domain.getBuild())
        data.add('decor', domain.getDecor())
        data.add('chunk', domain.getChunk())

        if domain.isMapLoaded():
            filterData = Common.Common_Filter({
                '_id': domain.getId()
            })
            self._update(data, filterData)
        else:
            data.add('_id', domain.getId())
            self._insert(data)

    def getById(self, queryId):
        result = self._select(
            Common.Common_Filter().setId(queryId),
            Common.Common_Limit().setOne()
        )

        if result is None:
            raise exceptions.database.NotFound('Data by _id %s not found in table `%s`' % (queryId, self._table))

        result['map_status'] = 1
        return result

    def getByIds(self, ids):
        result = super().getById(ids)
        for i in result:
            result[i]['map_status'] = 1

        return result

Map_Mapper = Map_Mapper_Main()
