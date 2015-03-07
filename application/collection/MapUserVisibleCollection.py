from . import Abstract

import service.Map
from models.MapUserVisible.Domain import MapUserVisible_Domain

class MapUserVisible_Collection(Abstract.AbstractCollection):
    domain = MapUserVisible_Domain
    def getMap(self):
        result = []

        for i in self:
            i._loaded = True
            result.append(i.getPosId())

        return service.Map.Service_Map().getByPosIds(result)
