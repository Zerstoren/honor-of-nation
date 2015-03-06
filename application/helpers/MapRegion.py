import exceptions.args
from models.Map.Domain import Map_Domain

from helpers.MapCoordinate import MapCoordinate

class MapRegion(object):
    def __init__(self, fromX, toX, fromY, toY):
        self.fromX = int(fromX)
        self.toX = int(toX)
        self.fromY = int(fromY)
        self.toY = int(toY)

        if not 0 <= self.fromX <= 1999 or\
            not 0 <= self.toX <= 1999 or\
            not 0 <= self.fromY <= 1999 or\
            not 0 <= self.toY <= 1999 or\
            self.fromX > self.toX or\
            self.fromY > self.toY:
            raise exceptions.args.Arguments('Переданы неверные координаты')

    def getFromX(self):
        return self.fromX

    def getFromY(self):
        return self.fromY

    def getToX(self):
        return self.toX

    def getToY(self):
        return self.toY

    def getCollection(self):
        from collection import MapCollection
        mapCollection = MapCollection.Map_Collection()

        for y in range(self.fromY, self.toY + 1):
            for x in range(self.fromX, self.toX + 1):
                mapCoordinate = MapCoordinate(x=x, y=y)
                domain = Map_Domain()
                domain.setId(mapCoordinate.getPosId())

                mapCollection.append(domain)

        mapCollection.extract()
        return mapCollection

    def toObject(self):
        return {
            'fromX': self.fromX,
            'fromY': self.fromY,
            'toX': self.toX,
            'toY': self.toY
        }

