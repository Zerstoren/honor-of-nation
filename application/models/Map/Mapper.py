import models.Abstract.Mapper
from . import Common

class Map_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'map'

    def add(self, data):
        """
        :type data: dict
        """
        pass

    # def getByUserAndChunks(self, user, chunks):
    #     where = Common.Common_Filter({
    #
    #     })
    #
    #     result = self._select(where)

Map_Mapper = Map_Mapper_Main()
