
class Decorate():
    def packDomainToDict(self, resourceDomain):
        """
        :type resourceDomain: models.Resources.Domain.Resources_Domain
        """

        return {
            '_id': str(resourceDomain.getId()),
            'user': str(resourceDomain.getUser().getId()),
            'rubins': int(resourceDomain.getRubins()),
            'wood': int(resourceDomain.getWood()),
            'steel': int(resourceDomain.getSteel()),
            'stone': int(resourceDomain.getStone()),
            'eat': int(resourceDomain.getEat()),
            'gold': int(resourceDomain.getGold())
        }

    def getResources(self, userDomain):
        domain = super().getResources(userDomain)
        return self.packDomainToDict(domain)