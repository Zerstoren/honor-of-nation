from .Abstract import AbstractService
import models.Resources.Mapper
import models.Resources.Domain
import models.Resources.Common

from service.Town import Service_Town

class Service_Resources(AbstractService.Service_Abstract):
    def getResources(self, userDomain, user=None):
        """
        :type userDomain: models.User.Domain.User_Domain
        """
        domain = models.Resources.Domain.Resources_Domain()
        domain.setOptions(
            models.Resources.Mapper.Resources_Mapper.getByUser(userDomain)
        )

        return domain

    def setResources(self, user, resources):
        """
        :type user: models.User.Domain.User_Domain
        """
        resourcesDomain = user.getResources()
        resourcesDomain.setRubins(resources[models.Resources.Common.RUBINS])
        resourcesDomain.setWood(resources[models.Resources.Common.WOOD])
        resourcesDomain.setStone(resources[models.Resources.Common.STONE])
        resourcesDomain.setSteel(resources[models.Resources.Common.STEEL])
        resourcesDomain.setEat(resources[models.Resources.Common.EAT])
        resourcesDomain.setGold(resources[models.Resources.Common.GOLD])

        resourcesDomain.getMapper().save(resourcesDomain)

    def updateResource(self, user, part):
        userResourcesDomain = user.getResources()
        rubins, wood, steel, stone, eat = (0, 0, 0, 0, 0)

        for town in Service_Town().getUserTownsCollection(user):
            rubinsR, woodR, steelR, stoneR, eatR = self._updateResources(town, part)

            rubins += rubinsR
            wood += woodR
            steel += steelR
            stone += stoneR
            eat += eatR

        userResourcesDomain.upResources({
            models.Resources.Common.RUBINS: rubins,
            models.Resources.Common.WOOD: wood,
            models.Resources.Common.STONE: stone,
            models.Resources.Common.STEEL: steel,
            models.Resources.Common.EAT: eat
        })
        userResourcesDomain.getMapper().save(userResourcesDomain)

    def _updateResources(self, town, part):
        townResourcesDomain = town.getResourcesUp()

        rubins = int((townResourcesDomain.getRubins() + townResourcesDomain.getTax()) / part)
        wood = int(townResourcesDomain.getWood() / part)
        steel = int(townResourcesDomain.getSteel() / part)
        stone = int(townResourcesDomain.getStone() / part)
        eat = int(townResourcesDomain.getEat() / part)

        return (rubins, wood, steel, stone, eat, )

    def decorate(self, *args):
        """
        :rtype: Service_Resources
        """
        return super().decorate(*args)
