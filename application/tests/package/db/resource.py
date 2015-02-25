import models.MapResources.Domain
import models.Resources.Common as Common
import models.Map.Math

from tests.package.abstract import AbstractDeclaration

class Resource(AbstractDeclaration):
    TYPE_RESOURCE_RUBINS = Common.RUBINS
    TYPE_RESOURCE_WOOD = Common.WOOD
    TYPE_RESOURCE_STEEL = Common.STEEL
    TYPE_RESOURCE_STONE = Common.STONE
    TYPE_RESOURCE_EAT = Common.EAT

    def addResource(self, x, y, resourceType, user=None, town=None, amount=None, baseOutput=None):
        domain = models.MapResources.Domain.MapResources_Domain()
        domain.setPosId(models.Map.Math.fromPositionToId(x, y))
        domain.setType(resourceType)
        domain.setUser(user.getId() if user else None)
        domain.setTown(town.getId() if user else None)
        domain.setAmount(amount if amount is not None else self.getRandomInt(10000, 1000000))
        domain.setBaseOutput(baseOutput if baseOutput is not None else self.getRandomInt(1000, 10000))
        domain.setOutput(domain.getBaseOutput())
        domain.getMapper().save(domain)

        return domain
