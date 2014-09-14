from . import abstractGeneric
import hashlib
import random

import service.Map
import service.MapUserVisible

import models.MapResources.Domain
import models.Map.Math


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
        service.Map.Service_Map().fillCoordinate({
            'fromX': fromX,
            'fromY': fromY,
            'toX': toX,
            'toY': toY
        }, land, 0)

        return service.Map.Service_Map().getRegion(
            fromX,
            fromY,
            toX,
            toY
        )

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