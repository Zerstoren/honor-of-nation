from battle.places.field import Field
from battle.places.castle import Castle

from models.Map import Common as MapCommon

class PlacesFactory(object):
    @staticmethod
    def getPlace(mapDomain):
        buildType = mapDomain.getBuild()
        landType = mapDomain.getLand()

        if landType == MapCommon.LAND_VALLEY:
            return Field.getInstance()
        elif landType == MapCommon.LAND_STEPPE:
            return Field.getInstance()
        elif landType == MapCommon.LAND_SWAMP:
            return Field.getInstance()
        elif landType == MapCommon.LAND_FOREST:
            return Field.getInstance()
        elif landType == MapCommon.LAND_JUNGLE:
            return Field.getInstance()
        elif landType == MapCommon.LAND_MOUNTAINS:
            return Field.getInstance()
