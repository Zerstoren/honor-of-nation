import models.Abstract.Factory

from . import Domain
from . import Mapper


class TownBuilds_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getByTown(self, town):
        result = Mapper.TownBuilds_Mapper.getByTownId(town.getId())
        return self.getDomainFromData(result)

    def getDomainFromData(self, data):
        domain = Domain.TownBuilds_Domain()
        domain.setOptions(data)

        return domain

TownBuilds_Factory = TownBuilds_Factory_Main()
