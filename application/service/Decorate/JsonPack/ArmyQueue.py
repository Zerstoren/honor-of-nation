from service.Equipment.Units import Service_Equipment_Units

"""
Access Layer Level for decorate base service class
"""
class Decorate():
    def _pack(self, domain):
        return {
            '_id': str(domain.getId()),
            'town': str(domain.getTown().getId()),
            'unit': str(domain.getUnit().getId()),
            'count': int(domain.getCount()),
            'complete_after': domain.getCompleteAfter(),
            'start_at': domain.getStartAt(),
            'unit_data': Service_Equipment_Units().decorate(Service_Equipment_Units.JSONPACK)
                .get(domain.getUnit().getId())
        }

    def getQueue(self, town, user=None):
        result = super().getQueue(town, user)
        data = []
        for i in result:
            data.append(
                self._pack(i)
            )

        return data
