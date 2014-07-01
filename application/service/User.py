import service.Abstract.AbstractService
import models.User.Factory
import models.User.Mapper
import exceptions.database


class Service_User(service.Abstract.AbstractService.Service_Abstract):

    def login(self, login, password):
        """
        :rtype: models.User.Domain.User_Domain
        """

        try:
            userDomain = models.User.Factory.User_Factory.getDomainFromData(
                models.User.Mapper.User_Mapper.getByLogin(login)
            )
        except exceptions.database.NotFound:
            return (False, None, )

        if userDomain.passwordEqual(password):
            return (True, userDomain, )
        else:
            return (False, None, )

    def getUserDomain(self, domainId):
        return models.User.Factory.User_Factory.getDomainFromData(
            models.User.Mapper.User_Mapper.getById(domainId)
        )

    def decorate(self, *args):
        """
        :rtype: Service_User
        """
        return super().decorate(*args)
