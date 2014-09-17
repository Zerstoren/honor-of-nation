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
            return False

        if userDomain.passwordEqual(password):
            return userDomain
        else:
            return False

    def getUserDomain(self, domainId):
        return models.User.Factory.User_Factory.getDomainFromData(
            models.User.Mapper.User_Mapper.getById(domainId)
        )

    def searchUser(self, login):
        """
        :rtype: models.User.Domain.User_Domain
        """
        return models.User.Factory.User_Factory.getDomainFromData(
            models.User.Mapper.User_Mapper.searchUser(login)
        )

    def getAllUsers(self):
        return models.User.Factory.User_Factory.getCollectionFromDataNoCache(
            models.User.Mapper.User_Mapper.getAllUsersLogin()
        )

    def decorate(self, *args):
        """
        :rtype: Service_User
        """
        return super().decorate(*args)
