import models.Abstract.Factory

from . import Domain
from . import Mapper


class MapResources_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainByPosition(self, mapCoordinate):

        return self.getDomainFromData(
            Mapper.MapResources_Mapper.getResourceByPosition(mapCoordinate)
        )

    def getDomainFromData(self, data):
        domain = Domain.MapResources_Domain()
        domain.setOptions(data)
        return domain

    def getDomainById(self, _id):
        return self.getDomainFromData(
            Mapper.MapResources_Mapper.getById(_id)
        )

MapResources_Factory = MapResources_Factory_Main()
