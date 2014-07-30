
class Decorate():
    def _getJsonFromDomain(self, domain):
        """
        :type domain: models.Map.Domain.Map_Domain
        """
        return {
            'pos_id': domain.getPosId(),
            'chunk': domain.getChunk(),
            'x': domain.getX(),
            'y': domain.getY(),
            'land': domain.getLand(),
            'land_type': domain.getLandType(),
            'decor': domain.getDecor(),
            'build': domain.getBuild(),
            'build_type': domain.getBuildType()
        }

    def getByVisibleCollection(self, collection):
        mapCollection = super(Decorate, self).getByVisibleCollection(collection)
        result = []

        for i in mapCollection:
            result.append(self._getJsonFromDomain(i))

        return result
