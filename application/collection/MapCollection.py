from . import Abstract

import service.MapUserVisible
from models.Map.Domain import Map_Domain

class Map_Collection(Abstract.AbstractCollection):
    domain = Map_Domain

    def getMapVisible(self, user):
        result = []

        for i in self:
            result.append(i.getId())

        return service.MapUserVisible.Service_MapUserVisible().getByIds(user, result)

