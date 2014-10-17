import models.Abstract.Domain
from .Mapper import Map_Mapper

import models.MapResources.Factory

import helpers.MapCoordinate

class Map_Domain(models.Abstract.Domain.Abstract_Domain):
    def getResource(self):
        return models.MapResources.Factory.MapResources_Factory.getDomainByPosition(
            self.getPosition()
        )

    def getPosition(self):
        return helpers.MapCoordinate.MapCoordinate(x=self.getX(), y=self.getY())

    def getMapper(self):
        return Map_Mapper

    def extract(self, force=False):
        if not self.isMapLoaded():
            return self

        return super().extract(force)

    def isMapLoaded(self):
        return 'map_status' in self._domain_data

    def isBusyByBuild(self):
        return self.getBuild() != 0
