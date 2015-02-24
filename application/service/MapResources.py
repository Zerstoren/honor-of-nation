from .Abstract import AbstractService

import models.MapResources.Factory
import models.MapResources.Mapper
import models.MapResources.Domain

import models.Map.Math
import models.Map.Common

class Service_MapResources(AbstractService.Service_Abstract):

    def getResourceByPosition(self, mapCoordinate, user=None):
        return models.MapResources.Factory.MapResources_Factory.getDomainByPosition(mapCoordinate)

    def getResourceByTown(self, town, user=None):
        return models.MapResources.Factory.MapResources_Factory.getCollectionByTown(town)

    def getAllResources(self):
        return models.MapResources.Factory.MapResources_Factory.getAll()

    def saveResources(self, data):
        domain = models.MapResources.Factory.MapResources_Factory.getDomainFromData(data)
        domain.getMapper().save(domain)

        return True

    def resourceDown(self, resource):
        output = resource.getOutput()
        amount = resource.getAmount()
        resource.setAmount(amount - output)
        resource.getMapper().save(resource)


    def _calculateOutput(self, baseOutput):
        return baseOutput

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_MapResources
        """
        return super().decorate(*args)
