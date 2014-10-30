import models.Abstract.Mapper
from . import Common


class TownBuildsQueue_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    def getByTownAndKey(self, townDomain, key):
        commonFilter = Common.Common_Filter()
        commonFilter.add('town', townDomain.getId())
        commonFilter.add('key', key)

        commonOrder = Common.Common_Order()
        commonOrder.add('level', commonOrder.ASC)

        return self._select(commonFilter, None)

    # def getCurrent(self, buildDomain):
    #     commonFilter = Common.Common_Filter()
    #     commonFilter.add('town', buildDomain.getTown().getId())
    #     commonFilter.add('key', buildDomain.getKey())


    # def getChain(self, buildDomain):
    #     commonFilter = Common.Common_Filter()
    #     commonFilter.add('town', buildDomain.getTown().getId())
    #     commonFilter.add('key', buildDomain.getKey())
    #
    #     commonSort = Common.Common_Order()
    #     commonSort.add('level', commonSort.ASC)
    #
    #     return self._select(commonFilter, None, commonSort)

    def save(self, domain):
        commonSet = Common.Common_Set()
        commonSet.add('town', domain.getTown())
        commonSet.add('key', domain.getKey())
        commonSet.add('level', domain.getLevel())
        commonSet.add('complete_after', domain.getCompleteAfter())
        commonSet.add('queue_code', domain.getQueueCode())

        if domain.hasId():
            commonFilter = Common.Common_Filter()
            commonFilter.setId(domain.getId())
            self._update(commonSet, commonFilter)
        else:
            inserId = self._insert(commonSet)
            domain.setId(inserId)


TownBuildsQueue_Mapper = TownBuildsQueue_Mapper_Main()
