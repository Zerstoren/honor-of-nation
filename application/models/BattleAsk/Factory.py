import models.Abstract.Factory

from . import Domain
from . import Mapper


class BattleAsk_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def get(self, battleAskId):
        domain = Domain.BattleAsk_Domain()
        domain.setId(battleAskId)

        return domain

    def getByLocation(self, mapCoordinate):
        data = Mapper.BattleAsk_Mapper.getByMapPosition(mapCoordinate)
        return self._getDomainFromData(data)

    def _getDomainFromData(self, data):
        domain = Domain.BattleAsk_Domain()
        domain.setLocation(data['location'])
        domain.setAttacker(data['attacker'])
        domain.setDefender(data['defender'])

        return domain

BattleAsk_Factory = BattleAsk_Factory_Main()
