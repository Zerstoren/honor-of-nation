from .Abstract import AbstractService

import config

from models.Map.Factory import Map_Factory
import models.Map.Mapper
import models.Map.Math
import models.Map.Domain

import helpers.MapCoordinate

import exceptions.database


class Service_Map(AbstractService.Service_Abstract):
    def getByPosition(self, mapCoordinate):
        """
        :type mapPosition: helpers.MapCoordinate.MapCoordinate
        :rtype: models.Map.Domain.Map_Domain
        """
        return models.Map.Factory.Map_Factory.getDomainById(mapCoordinate.getPosId())

    def getByVisibleCollection(self, collection):
        """
        :type collection: collection.MapUserVisibleCollection.MapUserVisible_Collection
        """
        return collection.getMap()

    def getByPosIds(self, posIds):
        return Map_Factory.getByPosIds(posIds)

    def getRegion(self, regionMap):
        """
        :type regionMap:helpers.MapRegion.MapRegion
        """
        return Map_Factory.getRegion(regionMap)

    def fillCoordinate(self, regionMap, land, landType):
        """
        :type regionMap:helpers.MapRegion.MapRegion
        """

        for x in range(regionMap.getFromX(), regionMap.getToX() + 1):
            for y in range(regionMap.getFromY(), regionMap.getToY() + 1):
                mapCoordinate = helpers.MapCoordinate.MapCoordinate(x=x, y=y)
                domain = self._getDomainFromData(mapCoordinate.getX(), mapCoordinate.getY(), land, landType)
                domain.setId(mapCoordinate.getPosId())
                domain.getMapper().save(domain)

        return True

    def fillChunks(self, chunks, land, landType):
        for chunk in chunks:
            fromX, fromY = models.Map.Math.fromChunkToPosition(chunk)
            for x in range(fromX, fromX + int(config.get('map.chunk'))):
                for y in range(fromY, fromY + int(config.get('map.chunk'))):
                    mapCoordinate = helpers.MapCoordinate.MapCoordinate(x=x, y=y)
                    domain = self._getDomainFromData(mapCoordinate.getX(), mapCoordinate.getY(), land, landType)
                    domain.setId(mapCoordinate.getPosId())
                    domain.getMapper().save(domain)

        return True

    def _getDomainFromData(self, x, y, land, landType, decor=0, build=0, buildType=0):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        try:
            domain = models.Map.Factory.Map_Factory.getDomainById(
                helpers.MapCoordinate.MapCoordinate(x=x, y=y).getPosId()
            )
            domain.setLand(land)
            domain.setLandType(landType)
            return domain

        except exceptions.database.NotFound:
            return models.Map.Factory.Map_Factory.getDomainFromData({
                'pos_id': '',
                'chunk': '',
                'x': '',
                'y': '',
                'land': '',
                'land_type': '',
                'decor': '',
                'build': '',
                'bild_type': ''

            })

    def decorate(self, *args):
        """
        :rtype: Service_Map
        """
        return super().decorate(*args)
