from . import Abstract

import service.Map

class MapUserVisible_Collection(Abstract.AbstractCollection):
    def getMap(self):
        result = []

        for i in self:
            i._loaded = True
            result.append(i.getPosId())

        return service.Map.Service_Map().getByPosIds(result)
