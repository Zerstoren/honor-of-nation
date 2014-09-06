from .Abstract import AbstractService

import models.MapResources.Factory
import models.MapResources.Mapper

class Service_MapResources(AbstractService.Service_Abstract):

    def getResourceByPosition(self, x, y):
        resource = models.MapResources.Mapper.MapResources_Mapper.getResourceByPosition(x, y)

        if resource is False:
            return False

        return models.MapResources.Factory.MapResources_Factory.getDomainFromData(resource)

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_MapResources
        """
        return super().decorate(*args)
