import exceptions.args

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

    def toObject(self):
        return {
            'fromX': self.fromX,
            'fromY': self.fromY,
            'toX': self.toX,
            'toY': self.toY
        }

