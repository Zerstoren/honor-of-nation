import models.Abstract.Domain
from .Mapper import Map_Mapper


class Map_Domain(models.Abstract.Domain.Abstract_Domain):
    def getMapper(self):
        return Map_Mapper
