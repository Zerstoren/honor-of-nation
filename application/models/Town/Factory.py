import models.Abstract.Factory

from . import Domain
from . import Mapper


class Town_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getByPosition(self, mapCoordinate):
        result = Mapper.Town_Mapper.getByPosition(mapCoordinate)
        return self.getDomainFromData(result)

    def getDomainFromData(self, data):
        domain = Domain.MapResources_Domain()
        domain.setOptions(data)
        domain.setUser(data['user'])

        return domain

Town_Factory = Town_Factory_Main()
