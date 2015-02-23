import models.Abstract.Factory

from . import Domain
from . import Mapper


class TownResources_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, town):
        domain = Domain.TownResources_Domain()
        result = Mapper.TownResources_Mapper.get(town)

        return domain.setOptions(result)

TownResources_Factory = TownResources_Factory_Main()
