
class Decorate():
    def packDomainToDict(self, resourceDomain):
        """
        :type resourceDomain: models.Resources.Domain.Resources_Domain
        """

        return {
            'rubins': resourceDomain.getRubins(),
            'wood': resourceDomain.getWood(),
            'steel': resourceDomain.getSteel(),
            'stone': resourceDomain.getStone(),
            'eat': resourceDomain.getEat(),
            'gold': resourceDomain.getGold()
        }

    def getResources(self, transferUser, userDomain):
        domain = super().getResources(transferUser, userDomain)
        return self.packDomainToDict(domain)