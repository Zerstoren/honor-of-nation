
"""
Access Layer Level for decorate base service class
"""
class Decorate():
    def _pack(self, domain):
        return {
            '_id': str(domain.getId()),
            'town': domain.getTown().getId(),
            'unit': domain.getUnit().getId(),
            'count': domain.getCount(),
            'complete_after': domain.getCompleteAfter(),
            'start_at': domain.getStartAt()
        }

    def getQueue(self, town, user=None):
        result = super().getQueue(town, user)
        data = []
        for i in result:
            data.append(
                self._pack(i)
            )

        return data
