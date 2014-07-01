import models.Abstract.Factory
from . import Domain
from . import Mapper

class Map_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainById(self, userId):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        domain = self.getDomainFromData(
            Mapper.Map_Mapper.getById(userId)
        )

        return domain

    def getCollectionByUserAndChunks(self, user, chunksList):
        return Mapper.Map_Mapper.getByUserAndChunks(
            user,
            chunksList
        )

    def getDomainFromData(self, data):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        domain = Domain.Map_Domain()
        domain.setOptions(data)
        return domain

Map_Factory = Map_Factory_Main()
