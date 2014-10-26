import models.Abstract.Mapper

from . import Common

class TownBuilds_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    def getByTownId(self, townId):
        filterQuery = Common.Common_Filter()
        filterQuery.add('town', townId)

        filterLimit = Common.Common_Limit()
        filterLimit.setOne()

        return self._select(filterQuery, filterLimit)

    def getDefaultData(self):
        return {
            Common.BUILD_FIELD : 0,
            Common.BUILD_FARM : 0,
            Common.BUILD_MILL : 0,
            Common.BUILD_MINE : 0,
            Common.BUILD_ROAD : 0,
            Common.BUILD_STORAGE : 0,
            Common.BUILD_V_COUNCIL : 0,
            Common.BUILD_T_COUNCIL : 0,
            Common.BUILD_HEADQUARTERS : 0,
            Common.BUILD_GUILDHALL : 0,
            Common.BUILD_HUT : 0,
            Common.BUILD_HOUSE : 0,
            Common.BUILD_SMITHY : 0,
            Common.BUILD_CASERN : 0,
            Common.BUILD_BARRACK : 0,
            Common.BUILD_PRISON : 0,
            Common.BUILD_HIGH_WALL : 0,
            Common.BUILD_WALL : 0
        }

    def save(self, domain, town):
        commonSet = Common.Common_Set()
        commonSet\
            .add('town', town.getId())\
            .add(Common.BUILD_FIELD, domain.getField())\
            .add(Common.BUILD_FARM, domain.getFarm())\
            .add(Common.BUILD_MILL, domain.getMill())\
            .add(Common.BUILD_MINE, domain.getMine())\
            .add(Common.BUILD_ROAD, domain.getRoad())\
            .add(Common.BUILD_STORAGE, domain.getStorage())\
            .add(Common.BUILD_V_COUNCIL, domain.getVCouncil())\
            .add(Common.BUILD_T_COUNCIL, domain.getTCouncil())\
            .add(Common.BUILD_HEADQUARTERS, domain.getHeadquarters())\
            .add(Common.BUILD_GUILDHALL, domain.getGuildhall())\
            .add(Common.BUILD_HUT, domain.getHut())\
            .add(Common.BUILD_HOUSE, domain.getHouse())\
            .add(Common.BUILD_SMITHY, domain.getSmithy())\
            .add(Common.BUILD_CASERN, domain.getCasern())\
            .add(Common.BUILD_BARRACK, domain.getBarrack())\
            .add(Common.BUILD_PRISON, domain.getPrison())\
            .add(Common.BUILD_HIGH_WALL, domain.getHighWall())\
            .add(Common.BUILD_WALL, domain.getWall())

        if domain.hasId():
            filterQuery = Common.Common_Filter()
            filterQuery.setId(domain.getId())
            self._update(commonSet, filterQuery)
        else:
            townBuildsId = self._insert(commonSet)
            domain.setId(townBuildsId)


TownBuilds_Mapper = TownBuilds_Mapper_Main()
