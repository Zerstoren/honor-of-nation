import models.Abstract.Domain
from .Mapper import ArmyQueue_Mapper

from models.Equipment.Units.Domain import Equipment_Units_Domain
import models.Equipment.Units.Factory

import models.User.Factory

import models.Town.Factory
import models.Town.Domain


class ArmyQueue_Domain(models.Abstract.Domain.Abstract_Domain):
    def setUnit(self, unit):
        if isinstance(unit, Equipment_Units_Domain):
            self._domain_data['unit'] = unit.getId()
        else:
            self._domain_data['unit'] = unit

    def getUnit(self):
        unitId = self.get('unit')
        return models.Equipment.Units.Factory.Equipment_Units_Factory.get(unitId, True)

    def getTown(self):
        return models.Town.Factory.Town_Factory.getDomainById(
            self._domain_data['town']
        )

    def setTown(self, town):
        if isinstance(town, models.Town.Domain.Town_Domain):
            self._domain_data['town'] = town.getId()
        else:
            self._domain_data['town'] = town

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return ArmyQueue_Mapper
