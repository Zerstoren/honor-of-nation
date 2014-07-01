import models.Abstract.Domain
from .Mapper import MapUserVisible_Mapper


class MapUserVisible_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return MapUserVisible_Mapper
