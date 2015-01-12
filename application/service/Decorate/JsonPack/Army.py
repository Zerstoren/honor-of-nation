from service.Equipment.Units import Service_Equipment_Units


class Decorate():
    def _pack(self, domain):
        """
        :param domain: models.Army.Domain.Army_Domain
        :return:
        """
        unitService = Service_Equipment_Units().decorate(Service_Equipment_Units.JSONPACK)

        return {
            'user': str(domain.getUser().getId()),
            'unit': str(domain.getUnit().getId()),
            'unit_data': unitService.get(domain.getUnit().getId()),
            'commander': str(domain.getCommander().getId()) if domain.getCommander() else None,
            'count': domain.getCount(),
            'location': int(domain.getMap().getId())
        }

    def load(self, armyUser, position, user=None):
        collection = super().load(armyUser, position, user)
        result = []

        for i in collection:
            result.append(self._pack(i))

        return result
