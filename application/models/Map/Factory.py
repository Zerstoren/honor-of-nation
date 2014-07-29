import models.Abstract.Factory
from collection import MapCollection

from . import Domain
from . import Mapper
from . import Math

class Map_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainByPosition(self, x, y):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        domain = self.getDomainFromData(
            Mapper.Map_Mapper.getByPositionId(
                Math.fromPositionToId(x, y)
            )
        )

        return domain

    def getDomainById(self, domainId):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        domain = self.getDomainFromData(
            Mapper.Map_Mapper.getById(domainId)
        )

        return domain

    def getByChunks(self, chunks):
        """
        :rtype: collection.MapCollection.Map_Collection
        """
        return self.getCollectionFromData(
            Mapper.Map_Mapper.getByChunks(chunks)
        )

    def getCollectionFromData(self, data):
        """
        :rtype: collection.MapCollection.Map_Collection
        """
        collection = MapCollection.Map_Collection()
        for i in data:
            collection.append(self.getDomainFromData(i))

        return collection

    def getDomainFromData(self, data):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        domain = Domain.Map_Domain()
        domain.setOptions(data)
        return domain

Map_Factory = Map_Factory_Main()
