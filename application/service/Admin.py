from .Abstract import AbstractService
import models.Map.Mapper
import models.Map.Math
import models.Map.Factory
import models.Map.Domain

import exceptions.database

import service.User

import config


class Service_Admin(AbstractService.Service_Abstract):
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

    def fillCoordinate(self, coordinate, land, landType, user=None):
        land = int(land)
        landType = int(landType)

        for x in range(coordinate['fromX'], coordinate['toX'] + 1):
            for y in range(coordinate['fromY'], coordinate['toY'] + 1):
                domain = self._getDomainFromData(x, y, land, landType)
                domain.getMapper().save(domain)

        return True

    def fillChunks(self, chunks, land, landType, user=None):
        land = int(land)
        landType = int(landType)

        for chunk in chunks:
            fromX, fromY = models.Map.Math.fromChunkToPosition(chunk)
            for x in range(fromX, fromX + int(config.get('map.chunk'))):
                for y in range(fromY, fromY + int(config.get('map.chunk'))):
                    domain = self._getDomainFromData(x, y, land, landType)
                    domain.getMapper().save(domain)

        return True

    def searchUser(self, userLogin, user):
        return service.User.Service_User().searchUser(userLogin)

    def decorate(self, *args):
        """
        :rtype: Service_Admin
        """
        return super().decorate(*args)
