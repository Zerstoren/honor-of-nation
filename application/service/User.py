import service.Abstract.AbstractService
import models.User.Factory
import models.User.Mapper

import models.UserState.Factory
import models.UserState.Mapper

import exceptions.database


class Service_User(service.Abstract.AbstractService.Service_Abstract):

    def createUser(self):
        pass

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

    def getUserStates(self, user):
        return models.UserState.Factory.UserState_Factory.getCollectionFromData(
            models.UserState.Mapper.UserState_Mapper.userStates(user)
        )

    def getUserState(self, userFrom, userTo):
        try:
            stateResult = models.UserState.Mapper.UserState_Mapper.userState(userFrom, userTo)
        except exceptions.database.NotFound:
            models.UserState.Mapper.UserState_Mapper.createBaseState(userFrom, userTo)
            stateResult = models.UserState.Mapper.UserState_Mapper.userState(userFrom, userTo)

        return models.UserState.Factory.UserState_Factory.getDomainFromData(stateResult)

    def setUserState(self, userFrom, userTo, state):
        models.UserState.Mapper.UserState_Mapper.updateBaseState(userFrom, userTo, state)

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
