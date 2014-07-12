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
        collection = MapCollection.Map_Collection()
        result = Mapper.Map_Mapper.getByChunks(chunks)
        for i in result:
            domain = self.getDomainFromData(i)
            collection.append(domain)

        return collection


    def getDomainFromData(self, data):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        domain = Domain.Map_Domain()
        domain.setOptions(data)
        return domain

Map_Factory = Map_Factory_Main()
