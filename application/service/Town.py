import service.Abstract.AbstractService

import models.Town.Factory

class Service_Town(service.Abstract.AbstractService.Service_Abstract):
    def loadByPosition(self, mapCoordinate):
        return models.Town.Factory.Town_Factory.getByPosition(mapCoordinate)

    def save(self, townData):
        domain = models.Town.Factory.Town_Factory.getDomainFromData(townData)
        domain.getMapper().save(domain)

        return domain

    def decorate(self, *args):
        """
        :rtype: Service_Town
        """
        return super().decorate(*args)
