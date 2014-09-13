import models.Abstract.Domain
from .Mapper import Map_Mapper

import models.MapResources.Factory

class Map_Domain(models.Abstract.Domain.Abstract_Domain):
    def getResource(self):
        return models.MapResources.Factory.MapResources_Factory.getDomainByPosition(
            self.getX(), self.getY()
        )

    def getMapper(self):
        return Map_Mapper
