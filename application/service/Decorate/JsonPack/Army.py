from service.Equipment.Units import Service_Equipment_Units
from service.User import Service_User

class Decorate():
    def pack(self, domain):
        """
        :param domain: models.Army.Domain.Army_Domain
        :return:
        """
        unitService = Service_Equipment_Units().decorate(Service_Equipment_Units.JSONPACK)

        return {
            '_id': str(domain.getId()),
            'user': Service_User().getDecorateClass(Service_User.JSONPACK).packDomainToDict(domain.getUser()),
            'unit': str(domain.getUnit().getId()),
            'unit_data': unitService.getForce(domain.getUnit().getId()),
            'suite': str(domain.getSuite().getId()) if domain.getSuite() else None,
            'commander': str(domain.getCommander().getId()) if domain.getCommander() else None,
            'count': domain.getCount(),
            'power': domain.getPower(),
            'last_power_update': domain.getLastPowerUpdate(),
            'move_path': domain.getMovePath(),
            'mode': domain.getMode(),
            'location': int(domain.getMap().getId())
        }

    def load(self, armyUser, position, config=None, user=None):
        collection = super().load(armyUser, position, config=config, user=user)
        result = []

        for i in collection:
            result.append(self.pack(i))

        return result

    def loadByMapCollection(self, mapCollection):
        collection = super().loadByMapCollection(mapCollection)
        result = []

        for domain in collection:
            result.append(self.pack(domain))

        return result

    def loadDetail(self, armyUser, _id, user=None):
        def deepPack(block):
            current = self.pack(block['current'])
            suite = self.pack(block['suite']) if block['suite'] else None
            sub_army = []

            if block['sub_army']:
                for domain in block['sub_army']:
                    sub_army.append(deepPack(domain))

            return {
                'current': current,
                'suite': suite,
                'sub_army': sub_army
            }

        result = super().loadDetail(armyUser, _id, user)
        return deepPack(result)
