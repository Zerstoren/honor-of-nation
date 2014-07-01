from .Abstract import AbstractService
import models.Resources.Mapper
import models.Resources.Domain


class Service_Resources(AbstractService.Service_Abstract):
    def getResources(self, transferUser, userDomain):
        """
        :type userDomain: models.User.Domain.User_Domain
        """
        domain = models.Resources.Domain.Resources_Domain()

        domain.setOptions(
            models.Resources.Mapper.Resources_Mapper.getByUser(userDomain)
        )

        return domain


    def decorate(self, *args):
        """
        :rtype: Service_Resources
        """
        return super().decorate(*args)
