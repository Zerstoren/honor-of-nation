import helpers.MapRegion
import service.Map
import service.MapUserVisible


class Terrain(object):
    def fillTerrain(self, fromX, fromY, toX, toY, land=0):
        region = helpers.MapRegion.MapRegion(
            fromX=fromX,
            fromY=fromY,
            toX=toX,
            toY=toY
        )
        service.Map.Service_Map().fillCoordinate(region, land, 0)

        return service.Map.Service_Map().getRegion(region)

    def openRegion(self, user, mapCollection):
        return service.MapUserVisible.Service_MapUserVisible().openRegion(user, mapCollection)