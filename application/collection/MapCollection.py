from . import Abstract

import service.MapUserVisible

class Map_Collection(Abstract.AbstractCollection):
    def getMapVisible(self, user):
        result = []

        for i in self:
            result.append(i.getId())

        return service.MapUserVisible.Service_MapUserVisible().getByIds(user, result)

