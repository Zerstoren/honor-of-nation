import models.Map.Common


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

    def _getJsonForMap(self, domain):
        return {
            models.Map.Common.TRANSFER_ALIAS_POS_ID: domain.getId(),
            models.Map.Common.TRANSFER_ALIAS_LAND: domain.getLand(),
            models.Map.Common.TRANSFER_ALIAS_LAND_TYPE: domain.getLandType(),
            models.Map.Common.TRANSFER_ALIAS_DECOR: domain.getDecor(),
            models.Map.Common.TRANSFER_ALIAS_BUILD: domain.getBuild()
        }

    def fromCollectionToList(self, mapCollection):
        result = {}

        for i in mapCollection:
            if i.getY() not in result:
                result[i.getY()] = {}

            result[i.getY()][i.getX()] = self._getJsonForMap(i)

        return result

    def getByVisibleCollection(self, collection):
        mapCollection = super(Decorate, self).getByVisibleCollection(collection)
        return self.fromCollectionToList(mapCollection)

