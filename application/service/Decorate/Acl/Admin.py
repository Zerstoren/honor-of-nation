import config
import exceptions.httpCodes
import exceptions.args
import exceptions.message


class Decorate():
    def _testAccessAdmin(self, user):
        if int(config.get('game.admin_mode')) is 0:
            raise exceptions.httpCodes.Page403('Нет доступы. Вы не администратор.')

        if user and user.getAdmin() is False:
            raise exceptions.httpCodes.Page403('Нет доступы. Вы не администратор.')

    def fillCoordinate(self, coordinate, land, landType, user=None):
        self._testAccessAdmin(user)
        return super().fillCoordinate(coordinate, land, landType, user)

    def fillChunks(self, chunks, land, landType, user=None):
        self._testAccessAdmin(user)
        return super().fillChunks(chunks, land, landType, user)

    def searchUser(self, userLogin, user):
        self._testAccessAdmin(user)

        userDomain = super().searchUser(userLogin, user)

        if userDomain and userDomain.getAdmin() is True and user.getId() != userDomain.getId():
            raise exceptions.httpCodes.Page403('Нельзя редактировать админов, кроме себя')

        return userDomain

    def openMapForUser(self, user, coordinate, aclUser=None):
        self._testAccessAdmin(aclUser)
        return super().openMapForUser(user, coordinate)

    def saveMapResources(self, user, domainData):
        self._testAccessAdmin(user)
        return super().saveMapResources(user, domainData)

    def saveTown(self, user, townData):
        self._testAccessAdmin(user)
        return super().saveTown(user, townData)

    def getAllUsers(self, user):
        self._testAccessAdmin(user)
        return super().getAllUsers(user)