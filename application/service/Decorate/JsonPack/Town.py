
class Decorate():
    def pack(self, domain):
        return {
            '_id' : str(domain.getId()),
            "type": domain.getType(),
            "user": str(domain.getUser().getId()),
            "population": domain.getPopulation(),
            "pos_id": domain.getPosId(),
            "name": domain.getName()
        }

    def getById(self, townId):
        return self.pack(
            super().getById(townId)
        )

    def loadByPosition(self, mapCoordinate):
        return self.pack(
            super().loadByPosition(mapCoordinate)
        )

    def save(self, townData):
        domain = super().save(townData)
        return self.pack(domain)