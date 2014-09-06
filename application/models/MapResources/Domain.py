import models.Abstract.Domain
from .Mapper import MapResources_Mapper


class MapResources_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return MapResources_Mapper
