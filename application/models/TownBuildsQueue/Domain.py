import models.Abstract.Domain

import models.Town.Factory
import models.Town.Domain

from .Mapper import TownBuildsQueue_Mapper


class TownBuildsQueue_Domain(models.Abstract.Domain.Abstract_Domain):
    def getTown(self):
        return models.Town.Factory.Town_Factory.getDomainById(self._domain_data['town'])

    def setTown(self, town):
        if isinstance(town, models.Town.Domain.Town_Domain()):
            self._domain_data['town'] = town.getId()
        else:
            self._domain_data['town'] = town

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return TownBuildsQueue_Mapper
