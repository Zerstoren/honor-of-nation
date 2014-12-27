import models.MapResources.Domain
import models.Map.Math

class Resource(object):
    def addResource(self, x, y, resourceType, user=None, town=None, amount=None, baseOutput=None):
        domain = models.MapResources.Domain.MapResources_Domain()
        domain.setPosId(models.Map.Math.fromPositionToId(x, y))
        domain.setType(resourceType)
        domain.setUser(user)
        domain.setTown(town)
        domain.setAmount(amount if amount is not None else self.getRandomInt(10000, 1000000))
        domain.setBaseOutput(baseOutput if baseOutput is not None else self.getRandomInt(1000, 10000))
        domain.setOutput(domain.getBaseOutput())
        domain.getMapper().save(domain)
