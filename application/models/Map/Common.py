import models.Abstract.Common
import helpers.MapCoordinate

TRANSFER_ALIAS_POS_ID = 'pi'
TRANSFER_ALIAS_LAND = 'l'
TRANSFER_ALIAS_LAND_TYPE = 'lt'
TRANSFER_ALIAS_DECOR = 'd'
TRANSFER_ALIAS_BUILD = 'b'
TRANSFER_ALIAS_BUILD_TYPE = 'bt'

LAND_VALLEY = 0
LAND_STEPPE = 1
LAND_SWAMP = 2
LAND_FOREST = 3
LAND_JUNGLE = 4
LAND_MOUNTAINS = 5

BUILD_EMPTY = 0
BUILD_RESOURCES = 1
BUILD_POSTS = 2
BUILD_FORTIFICATION = 3
BUILD_ROAD = 4
BUILD_TOWNS = 5
BUILD_RUINS = 6

class Common_Set(models.Abstract.Common.Common_Set):
    pass


class Common_Filter(models.Abstract.Common.Common_Filter):
    def setId(self, recordId):
        mapCoordinate = helpers.MapCoordinate.MapCoordinate(posId=recordId)
        self.add('_id', mapCoordinate.getPosId())
        return self


class Common_Limit(models.Abstract.Common.Common_Limit):
    pass


class Common_Order(models.Abstract.Common.Common_Order):
    pass
