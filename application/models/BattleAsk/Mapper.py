import models.Abstract.Mapper
import models.BattleAsk.Common as Common


class BattleAsk_Mapper_Main(models.Abstract.Mapper.Abstract_Mapper):
    _table = 'battle_ask'

    def getByMapPosition(self, mapCoordinate):
        commonSet = Common.Common_Set()
        commonSet.add('location', mapCoordinate.getPosId())

        commonLimit = Common.Common_Limit()
        commonLimit.setOne()

        return self._select(commonSet, commonLimit)

    def save(self, domain):
        commonSet = Common.Common_Set()
        commonSet.add('location', domain.getLocation())
        commonSet.add('attacker', domain.getAttacker())
        commonSet.add('defender', domain.getDefender())

        if domain.hasId():
            commonFilter = Common.Common_Filter()
            commonFilter.setId(domain.getId())
            self._update(commonSet, commonFilter)
        else:
            insertId = self._insert(commonSet)
            domain.setId(insertId)

        return domain

BattleAsk_Mapper = BattleAsk_Mapper_Main()
