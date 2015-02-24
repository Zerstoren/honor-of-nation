import models.Abstract.Domain
from .Mapper import TownResources_Mapper


class TownResources_Domain(models.Abstract.Domain.Abstract_Domain):
    def getTown(self):
        from service.Town import Service_Town
        return Service_Town().getById(self.get('town'))

    def setTown(self, town):
        from models.Town.Domain import Town_Domain
        if isinstance(town, Town_Domain):
            self.set('town', town.getId())
        else:
            self.set('town', town)

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return TownResources_Mapper
