import models.Abstract.Factory

from . import Domain
from . import Mapper

import collection.TownCollection

class Town_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainById(self, townId):
        domain = Domain.Town_Domain()
        domain.setId(townId)

        return domain

    def getByPosition(self, mapCoordinate):
        result = Mapper.Town_Mapper.getByPosition(mapCoordinate)
        return self.getDomainFromData(result)

    def getByUser(self, user):
        result = Mapper.Town_Mapper.getByUser(user)
        townCollection = collection.TownCollection.Town_Collection()
        townCollection.setOptions(result)

        return townCollection

    def getAll(self):
        result = Mapper.Town_Mapper.getAll()
        townCollection = collection.TownCollection.Town_Collection()
        townCollection.setOptions(result)

        return townCollection

    def getDomainFromData(self, data):
        domain = Domain.Town_Domain()
        domain.setOptions(data)
        domain.setUser(data['user'])

        return domain

Town_Factory = Town_Factory_Main()
