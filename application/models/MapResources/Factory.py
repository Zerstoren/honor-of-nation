import models.Abstract.Factory

from . import Domain
from . import Mapper


class MapResources_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainFromData(self, data):
        domain = Domain.MapResources_Domain()
        domain.setOptions(data)
        return domain

MapResources_Factory = MapResources_Factory_Main()
