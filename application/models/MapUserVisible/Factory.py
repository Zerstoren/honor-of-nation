import models.Abstract.Factory

from . import Domain
from . import Mapper

import collection.MapUserVisibleCollection

class MapUserVisible_Factory_Main(models.Abstract.Factory.Abstract_Factory):

    def getVisibleDomain(self, mapDomain, userDomain):
        """
        :type mapDomain: models.Map.Domain.Map_Domain
        :type userDomain: models.User.Domain.User_Domain
        """
        return self.getDomainFromData(
            Mapper.MapUserVisible_Mapper.getByPosition(mapDomain.getPosition(), userDomain)
        )

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

        collectionMapUserVisible = collection.MapUserVisibleCollection.MapUserVisible_Collection()

        for i in result:
            collectionMapUserVisible.append(
                self.getDomainFromData(i)
            )

        return collection

    def getCollectionFromData(self, data):
        """
        :rtype: collection.MapUserVisibleCollection.MapUserVisible_Collection
        """
        collectionMapUserVisible = collection.MapUserVisibleCollection.MapUserVisible_Collection()
        for i in data:
            collectionMapUserVisible.append(
                self.getDomainFromData(i)
            )

        return collectionMapUserVisible

    def getDomainFromData(self, data):
        """
        :rtype: models.MapUserVisible.Domain.MapUserVisible_Domain
        """
        domain = Domain.MapUserVisible_Domain()
        domain.setOptions(data)
        return domain

MapUserVisible_Factory = MapUserVisible_Factory_Main()
