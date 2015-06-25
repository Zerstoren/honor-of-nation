from .Abstract import AbstractService

from models.BattleAsk.Factory import BattleAsk_Factory


class Service_Battle(AbstractService.Service_Abstract):
    def acceptBattle(self, mapCoordinate, acceptUser, info, user=None):
        battleAskDomain = BattleAsk_Factory.getByLocation(mapCoordinate)
        state = 'attacker' if str(acceptUser.getId()) in battleAskDomain.getAttacker() else 'defender'

        result = battleAskDomain.get(state)[str(acceptUser.getId())]
        result['accept'] = info['accept']

        for unit in result['units']:
            unit['accept'] = info['units'][str(unit['unit'])]

        battleAskDomain.get(state)[str(acceptUser.getId())] = result

        battleAskDomain.getMapper().save(battleAskDomain)

    def addBattleAsk(self, mapCoordinate, attacker, defender):
        domain = BattleAsk_Factory.getDomainFromData({
            'location': mapCoordinate.getPosId(),
            'attacker': attacker,
            'defender': defender
        })

        domain.getMapper().save(domain)

        return domain

    def startBattle(self, battleAskId):
        battleAsk = BattleAsk_Factory.get(battleAskId)
        battleAsk.extract()
        print(battleAsk._domain_data)

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_Battle
        """
        return super().decorate(*args)
