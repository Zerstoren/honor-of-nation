import config
import exceptions.httpCodes

class Decorate():
    def _testAccessAdmin(self, user):
        if int(config.get('game.admin_mode')) is 0:
            raise exceptions.httpCodes.Page403('Can`t access to admin area')

        if user and user.getAdmin() is False:
            raise exceptions.httpCodes.Page403('Can`t access to admin area')

    def fillCoordinate(self, coordinate, land, landType, user=None):
        self._testAccessAdmin(user)
        return super().fillCoordinate(coordinate, land, landType, user)

    def fillChunks(self, chunks, land, landType, user=None):
        self._testAccessAdmin(user)
        return super().fillChunks(chunks, land, landType, user)