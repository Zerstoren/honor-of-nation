import service.Abstract.AbstractService

import models.TownBuilds.Factory


class Service_TownBuilds(service.Abstract.AbstractService.Service_Abstract):
    def get(self, townDomain, user):
        return models.TownBuilds.Factory.TownBuilds_Factory.getByTown(townDomain)

    def decorate(self, *args):
        """
        :rtype: Service_TownBuilds
        """
        return super().decorate(*args)
