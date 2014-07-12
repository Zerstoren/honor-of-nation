from .Abstract import AbstractService

import models.Map.Factory
import models.MapUserVisible.Factory


class Service_Map(AbstractService.Service_Abstract):
    def getUsersChunks(self, user, chunksList):
        collection = models.MapUserVisible.Factory.MapUserVisible_Factory.getCollectionCellsByUsers(
            user,
            chunksList
        )


    def decorate(self, *args):
        """
        :rtype: Service_Map
        """
        return super().decorate(*args)
