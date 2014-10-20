
class Decorate():
    def _pack(self, domain):
        return {
            '_id' : str(domain.getId()),
            "type": domain.getType(),
            "user": str(domain.getUser().getId()),
            "population": domain.getPopulation(),
            "pos_id": domain.getPosId(),
            "name": domain.getName()
        }

    def loadByPosition(self, mapCoordinate):
        return self._pack(
            super().loadByPosition(mapCoordinate)
        )

    def save(self, townData):
        domain = super().save(townData)
        return self._pack(domain)