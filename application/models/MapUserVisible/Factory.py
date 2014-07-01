import models.Abstract.Factory
from . import Domain
from . import Mapper
from collection import MapUserVisibleCollection

class MapUserVisible_Factory_Main(models.Abstract.Factory.Abstract_Factory):

    def getCollectionCellsByUsers(self, user, chunksList):
        """
        :type user: models.User.Domain.User_Domain
        :type chunksList: list
        :rtype: collection.Map_User_Visible.MapUserVisible_Collection
        """
        result = Mapper.MapUserVisible_Mapper.getCellsByUsersAndChunks(
            user,
            chunksList
        )

        collection = MapUserVisibleCollection.MapUserVisible_Collection()

        for i in result:
            collection.append(
                self.getDomainFromData(i)
            )

        return collection

    def getDomainFromData(self, data):
        """
        :rtype: models.Map.Domain.Map_Domain
        """
        domain = Domain.MapUserVisible_Domain()
        domain.setOptions(data)
        return domain

MapUserVisible_Factory = MapUserVisible_Factory_Main()
