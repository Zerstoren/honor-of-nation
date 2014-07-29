import models.Abstract.Mapper
from . import Common


class MapUserVisible_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map_user_visible'

    def getByIds(self, user, ids):
        queryFilter = Common.Common_Filter()
        queryFilter.addIn('_id', ids)
        queryFilter.add('user_id', user.getId())

        return self._select(queryFilter)

    def insertCollection(self, user, region):
        """
        :type user: models.User.Domain.User_Domain
        :type region: collection.MapCollection.Map_Collection
        """
        self.bulkStart()

        for i in region:
            commonSet = Common.Common_Set()
            commonSet.add('pos_id', i.getPosId())
            commonSet.add('chunk', i.getChunk())
            commonSet.add('user_id', user.getId())

            self._insert(commonSet)

        self.bulkEnd()

    def getCellsByUsersAndChunks(self, user, chunks):
        queryFilter = Common.Common_Filter()
        queryFilter.add('user_id', user.getId())
        queryFilter.addIn('chunk', chunks)

        return self._select(queryFilter)

MapUserVisible_Mapper = MapUserVisible_Mapper_Main()
