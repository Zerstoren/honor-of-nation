from . import abstractGeneric
import hashlib
import random

import service.Map
import service.MapUserVisible

import models.MapResources.Domain
import models.Town.Domain
import models.Map.Math

import models.TownBuilds.Factory
import models.TownBuilds.Mapper

import helpers.MapRegion
import helpers.MapCoordinate


class Generic(abstractGeneric.Abstract_Generic):
    def getRandomName(self, prefix='', length=8):
        return prefix + hashlib.md5(str(random.randint(0, 100000000)).encode()).hexdigest()[0:length]

    def getRandomInt(self, minimal=0, maximal=100, prefix=''):
        return prefix + str(random.randint(minimal, maximal)) if prefix else random.randint(minimal, maximal)

    def setUserAsAdmin(self, user):
        """
        :type user: models.User.Domain.User_Domain
        """
        user.setAdmin(True)
        user.getMapper().save(user)

    def fillTerrain(self, fromX, fromY, toX, toY, land=0):
        region = helpers.MapRegion.MapRegion(**{
            'fromX': fromX,
            'fromY': fromY,
            'toX': toX,
            'toY': toY
        })
        service.Map.Service_Map().fillCoordinate(region, land, 0)

        return service.Map.Service_Map().getRegion(region)

    def openRegion(self, user, mapCollection):
        return service.MapUserVisible.Service_MapUserVisible().openRegion(user, mapCollection)

    def addResource(self, x, y, resourceType, user=None, town=None, amount=None, baseOutput=None):
        domain = models.MapResources.Domain.MapResources_Domain()
        domain.setPosId(models.Map.Math.fromPositionToId(x, y))
        domain.setType(resourceType)
        domain.setUser(user)
        domain.setTown(town)
        domain.setAmount(amount if amount is not None else self.getRandomInt(10000, 1000000))
        domain.setBaseOutput(baseOutput if baseOutput is not None else self.getRandomInt(1000, 10000))
        domain.setOutput(domain.getBaseOutput())
        domain.getMapper().save(domain)

    def addTown(self, x, y, user, population=None, typeTown=0, name=None):
        population = population if population else self.getRandomInt(100, 10000)
        name = name if name else self.getRandomName('city-')
        mapCoordinate = helpers.MapCoordinate.MapCoordinate(x=x, y=y)

        domain = models.Town.Domain.Town_Domain()
        domain.setPosId(mapCoordinate.getPosId())
        domain.setName(name)
        domain.setType(typeTown)
        domain.setPopulation(population),
        domain.setUser(user)
        domain.getMapper().save(domain)

        buildsTownDomain = models.TownBuilds.Factory.TownBuilds_Factory.getDomainFromData(
            models.TownBuilds.Mapper.TownBuilds_Mapper.getDefaultData()
        )
        buildsTownDomain.setTown(domain)

        buildsTownDomain.getMapper().save(buildsTownDomain)
        return domain
