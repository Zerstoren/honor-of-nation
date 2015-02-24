import models.Abstract.Domain
from .Mapper import TownBonus_Mapper


class TownBonus_Domain(models.Abstract.Domain.Abstract_Domain):
    def getTown(self):
        from service.Town import Service_Town
        return Service_Town().getById(self.get('town'))

    def setTown(self, town):
        from models.Town.Domain import Town_Domain
        if isinstance(town, Town_Domain):
            self.set('town', town.getId())
        else:
            self.set('town', town)

    def reset(self):
        for key in self._domain_data:
            if key == '_id' or key == 'town':
                continue

            self._domain_data[key] = 0

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return TownBonus_Mapper
