import models.Abstract.Mapper
from . import Common


class MapUserVisible_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map_user_visible'

    def getCellsByUsersAndChunks(self, user, chunks):
        where = Common.Common_Filter({
            'user_id': user.getId(),
            'chunk': {
                '$in': chunks
            }
        })

        return self._select(where)

MapUserVisible_Mapper = MapUserVisible_Mapper_Main()
