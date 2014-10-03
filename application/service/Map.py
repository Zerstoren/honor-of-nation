from .Abstract import AbstractService

import config

import models.Map.Factory
import models.Map.Mapper
import models.Map.Math
import models.Map.Domain
import models.MapUserVisible.Factory

import exceptions.database


class Service_Map(AbstractService.Service_Abstract):
    def getByVisibleCollection(self, collection):
        """
        :type collection: collection.MapUserVisibleCollection.MapUserVisible_Collection
        """
        return collection.getMap()

    def getByPosIds(self, posIds):
        return models.Map.Factory.Map_Factory.getCollectionFromData(
            models.Map.Mapper.Map_Mapper.getByPosIds(posIds)
        )

    def getRegion(self, regionMap):
        """
        :type regionMap:helpers.MapRegion.MapRegion
        """
        regionResult = models.Map.Mapper.Map_Mapper.getRegion(regionMap)

        return models.Map.Factory.Map_Factory.getCollectionFromData(
            regionResult
        )

    def fillCoordinate(self, regionMap, land, landType):
        """
        :type regionMap:helpers.MapRegion.MapRegion
        """

        for x in range(regionMap.getFromX(), regionMap.getToX() + 1):
            for y in range(regionMap.getFromY(), regionMap.getToY() + 1):
                domain = self._getDomainFromData(x, y, land, landType)
                domain.getMapper().save(domain)

        return True

    def fillChunks(self, chunks, land, landType):
        for chunk in chunks:
            fromX, fromY = models.Map.Math.fromChunkToPosition(chunk)
            for x in range(fromX, fromX + int(config.get('map.chunk'))):
                for y in range(fromY, fromY + int(config.get('map.chunk'))):
                    domain = self._getDomainFromData(x, y, land, landType)
                    domain.getMapper().save(domain)

        return True

    def _getDomainFromData(self, x, y, land, landType, decor=0, build=0, buildType=0):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        try:
            domain = models.Map.Factory.Map_Factory.getDomainByPosition(x, y)
            domain.setLand(land)
            domain.setLandType(landType)
            return domain

        except exceptions.database.NotFound:
            domain = models.Map.Domain.Map_Domain()
            domain.setPosId(models.Map.Math.fromPositionToId(x, y))
            domain.setChunk(models.Map.Math.fromPositionToChunk(x, y))
            domain.setX(x)
            domain.setY(y)
            domain.setLand(land)
            domain.setLandType(landType)
            domain.setDecor(decor)
            domain.setBuild(build)
            domain.setBuildType(buildType)
            return domain

    def decorate(self, *args):
        """
        :rtype: Service_Map
        """
        return super().decorate(*args)
