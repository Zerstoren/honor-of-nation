import models.Map.Math

class MapCoordinate(object):
    def __init__(self, posId=None, x=None, y=None):
        if posId is not None:
            self.posId = int(posId)
            self.x, self.y = models.Map.Math.fromIdToPosition(self.posId)
        elif x is not None and y is not None:
            self.x = int(x)
            self.y = int(y)
            self.posId = models.Map.Math.fromPositionToId(x, y)
        else:
            raise Exception('Invalid MapCoordinate params')

        self.__validate()

    def getCoordinate(self):
        return (self.x, self.y, )

    def getPosId(self):
        return self.posId

    def __validate(self):
        if self.posId < 0 or self.posId > 2000 * 2000 - 1:
            raise Exception('Invalid position id coordinate %s' % str(self.posId))

        if not 0 <= self.x <= 1999 or not 0 <= self.y <= 1999:
            raise Exception('Invalid point position %sx%s' % (str(self.x), str(self.y)))