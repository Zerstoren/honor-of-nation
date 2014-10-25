import models.Abstract.Domain
from .Mapper import TownBuilds_Mapper


class TownBuilds_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return TownBuilds_Mapper
