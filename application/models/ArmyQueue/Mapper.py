import models.Abstract.Mapper

from . import Common


class ArmyQueue_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'army_queue'

    def save(self, domain):
        """
        :type domain: models.ArmyQueue.Domain.ArmyQueue_Domain
        """
        commonSet = Common.Common_Set()
        commonSet.add('town', domain.getTown().getId())
        commonSet.add('unit', domain.getUnit().getId())
        commonSet.add('count', domain.getCount())
        commonSet.add('complete_after', domain.getCompleteAfter())
        commonSet.add('start_at', domain.getStartAt())
        commonSet.add('queue_code', domain.getQueueCode())

        if domain.hasId():
            commonFilter = Common.Common_Filter()
            commonFilter.setId(domain.getId())
            self._update(commonSet, commonFilter)
        else:
            insertId = self._insert(commonSet)
            domain.setId(insertId)

    def load(self, town):
        commonFilter = Common.Common_Filter()
        commonFilter.add('town', town.getId())
        return self._select(commonFilter)


ArmyQueue_Mapper = ArmyQueue_Mapper_Main()
