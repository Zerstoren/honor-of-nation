
class Decorate():
    def _pack(self, domain):
        return {
            "type": domain.getType(),
            "user": str(domain.getUser().getId()),
            "population": domain.getPopulation(),
            "pos_id": domain.getPosId(),
            "name": domain.getName()
        }

    def loadByPosition(self, x, y):
        return self._pack(
            super().loadByPosition(x, y)
        )

    def save(self, townData):
        domain = super().save(townData)
        return self._pack(domain)