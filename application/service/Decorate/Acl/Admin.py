import config
import exceptions.httpCodes
import exceptions.args
import exceptions.message


class Decorate():
    def _testAccessAdmin(self, user):
        if int(config.get('game.admin_mode')) is 0:
            raise exceptions.httpCodes.Page403('Can`t access to admin area')

        if user and user.getAdmin() is False:
            raise exceptions.httpCodes.Page403('Can`t access to admin area')

    def fillCoordinate(self, coordinate, land, landType, user=None):
        """
        @param coordinate models.Map.Region.MapRegion
        @param land str
        @param landType str
        @param user models.User.Domain.UserDomain
        """
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

    # def openMapForUser(self, user, coordinate):
    #     self._testAccessAdmin(user)
    #     return super().openMapForUser(user, coordinate)