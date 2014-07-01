import models.Abstract.Common

LAND_VALLEY = 0
LAND_STEPPE = 1
LAND_SWAMP = 2
LAND_FOREST = 3
LAND_JUNGLE = 4
LAND_MOUNTAINS = 5

TRANSFER_ALIAS_POS_ID = 'pi'
TRANSFER_ALIAS_LAND = 'l'
TRANSFER_ALIAS_LAND_TYPE = 'lt'
TRANSFER_ALIAS_DECOR = 'd'
TRANSFER_ALIAS_BUILD = 'b'
TRANSFER_ALIAS_BUILD_TYPE = 'bt'

BUILD_EMPTY = 0
BUILD_RESOURCES = 1
BUILD_POSTS = 2
BUILD_FORTIFICATION = 3
BUILD_ROAD = 4
BUILD_TOWNS = 5
BUILD_RUINS = 6

class Common_Set(models.Abstract.Common.Common_Set):
    def posId(self, posId):
        if not 0 < posId < 4000000:
            raise Exception('Wrong position id')

        self.add('pos_id', posId)

        return self

    def x(self, x):
        if not 0 < x < 2000:
            raise Exception('Wrong `x` coordinate')

        self.add('x', x)
        return self

    def y(self, y):
        if not 0 < y < 2000:
            raise Exception('Wrong `y` coordinate')

        self.add('y', y)
        return self

    def chunk(self, chunk):
        if not 0 < chunk < 12525:
            raise Exception('Wrong chunk number')

        self.add('chunk', chunk)
        return self

    def land(self, land):
        if not land in (LAND_VALLEY, LAND_STEPPE, LAND_SWAMP, LAND_FOREST, LAND_JUNGLE, LAND_MOUNTAINS):
            raise Exception('Wrong land')

        self.add('land', land)
        return self

    def landType(self, landType):
        if not 0 < landType < 9:
            raise Exception('Wrong land type')

        self.add('land_type', landType)
        return self

    def decor(self, decor):
        self.add('decor', decor)
        return self

    def build(self, build):
        self.add('build', build)
        return self

    def buildType(self, buildType):
        self.add('build_type', buildType)
        return self


class Common_Filter(models.Abstract.Common.Common_Filter):
    pass


class Common_Limit(models.Abstract.Common.Common_Limit):
    pass


class Common_Order(models.Abstract.Common.Common_Order):
    pass
