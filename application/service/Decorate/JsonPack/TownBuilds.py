import models.Town.Common
from models.TownBuilds import Common

class Decorate():
    def _packVillage(self, domain):
        return {
            Common.BUILD_MILL: domain.getMill(),
            Common.BUILD_FIELD: domain.getField(),
            Common.BUILD_FARM: domain.getFarm(),
            Common.BUILD_MINE: domain.getMine(),
            Common.BUILD_ROAD: domain.getRoad(),
            Common.BUILD_V_COUNCIL: domain.getVCouncil(),
            Common.BUILD_HUT: domain.getHut()
        }

    def _packCity(self, domain):
        return {
            Common.BUILD_MILL: domain.getMill(),
            Common.BUILD_FIELD: domain.getField(),
            Common.BUILD_FARM: domain.getFarm(),
            Common.BUILD_MINE: domain.getMine(),
            Common.BUILD_ROAD: domain.getRoad(),
            Common.BUILD_STORAGE: domain.getStorage(),
            Common.BUILD_T_COUNCIL: domain.getTCouncil(),
            Common.BUILD_GUILDHALL: domain.getGuildhall(),
            Common.BUILD_HOUSE: domain.getHouse(),
            Common.BUILD_SMITHY: domain.getSmithy(),
            Common.BUILD_CASERN: domain.getCasern(),
            Common.BUILD_PRISON: domain.getPrison(),
            Common.BUILD_WALL: domain.getWall()
        }

    def _packCastle(self, domain):
        return {
            Common.BUILD_FARM: domain.getFarm(),
            Common.BUILD_MINE: domain.getMine(),
            Common.BUILD_ROAD: domain.getRoad(),
            Common.BUILD_HEADQUARTERS: domain.getHeadquarters(),
            Common.BUILD_BARRACK: domain.getBarrack(),
            Common.BUILD_SMITHY: domain.getSmithy(),
            Common.BUILD_CASERN: domain.getCasern(),
            Common.BUILD_HIGH_WALL: domain.getHighWall()
        }

    def get(self, townDomain, user):
        townBuilds = super().get(townDomain, user)

        if townDomain.getType() == models.Town.Common.VILLAGE:
            return self._packVillage(townBuilds)
        elif townDomain.getType() == models.Town.Common.CITY:
            return self._packCity(townBuilds)
        elif townDomain.getType() == models.Town.Common.CASTLE:
            return self._packCastle(townBuilds)
