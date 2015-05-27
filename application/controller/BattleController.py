from service.Battle import Service_Battle

class AbstractBattleController(object):
    def _getBattleService(self):
        return Service_Battle()

    def _getParamsBattleService(self):
        return Service_Battle().decorate(Service_Battle.PARAMS)

    def _getParamsAclBattleService(self):
        return Service_Battle().decorate(Service_Battle.PARAMS_ACL)


class MainController(AbstractBattleController):
    def acceptBattle(self, transfer, data):
        self._getParamsAclBattleService().acceptBattle(
            data['mapPosition'],
            data['user'],
            {
                'accept': data['accept'],
                'units': data['units']
            },
            transfer.getUser()
        )


class DeliveryController(AbstractBattleController):
    def askAboutBattle(self, mapCoordinate, attackerArmy, defenderArmy):
        from service.Army import Service_Army

        def parseArmy(mapCoordinate, army):
            armyJsonPack = Service_Army().getDecorateClass(Service_Army.JSONPACK)

            for userId in army:
                army[userId]['user'].getTransfer().forceSend('/delivery/askAboutBattle', {
                    'mapPosition': mapCoordinate.getPosId(),
                    'army': [armyJsonPack.pack(unit) for unit in army[userId]['units']],
                    'state': 'attack'
                })

        parseArmy(mapCoordinate, attackerArmy)
        parseArmy(mapCoordinate, defenderArmy)


class CeleryPrivateController(AbstractBattleController):
    def waitBattle(self, message):
        self._getParamsBattleService().startBattle(message)
