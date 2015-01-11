from .Abstract import AbstractService
import models.Resources.Mapper
import models.Resources.Domain
import models.Resources.Common

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


    def decorate(self, *args):
        """
        :rtype: Service_Resources
        """
        return super().decorate(*args)
