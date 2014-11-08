import service.Abstract.AbstractService
import models.TownBuilds.Factory
import models.TownBuilds.Mapper

import models.Town.Factory

class Service_Town(service.Abstract.AbstractService.Service_Abstract):
    def getById(self, townId):
        return models.Town.Factory.Town_Factory.getDomainById(townId)

    def loadByPosition(self, mapCoordinate):
        return models.Town.Factory.Town_Factory.getByPosition(mapCoordinate)

    def save(self, townData):
        domain = models.Town.Factory.Town_Factory.getDomainFromData(townData)
        domain.getMapper().save(domain)

        buildsTownDomain = models.TownBuilds.Factory.TownBuilds_Factory.getDomainFromData(
            models.TownBuilds.Mapper.TownBuilds_Mapper.getDefaultData()
        )
        buildsTownDomain.setTown(domain)

        buildsTownDomain.getMapper().save(buildsTownDomain)

        return domain

    def decorate(self, *args):
        """
        :rtype: Service_Town
        """
        return super().decorate(*args)
