import config
import exceptions.httpCodes
import exceptions.args

class Decorate():
    def _testAccessAdmin(self, user):
        if int(config.get('game.admin_mode')) is 0:
            raise exceptions.httpCodes.Page403('Can`t access to admin area')

        if user and user.getAdmin() is False:
            raise exceptions.httpCodes.Page403('Can`t access to admin area')

    def fillCoordinate(self, coordinate, land, landType, user=None):
        self._testAccessAdmin(user)
        #
        # if coordinate['fromX'] < 0 or coordinate['toX'] > 1999 or \
        #         coordinate['fromY'] < 0 or coordinate['toY'] > 1999:
        #     raise exceptions.args.Arguments('Wrong coordinate')

        if not 0 <= coordinate['fromX'] <= 1999 or\
            not 0 <= coordinate['toX'] <= 1999 or\
            not 0 <= coordinate['fromY'] <= 1999 or\
            not 0 <= coordinate['toY'] <= 1999 or\
            coordinate['fromX'] > coordinate['toX'] or\
            coordinate['fromY'] > coordinate['toY']:
            raise exceptions.args.Arguments('Wrong coordinate')

        return super().fillCoordinate(coordinate, land, landType, user)

    def fillChunks(self, chunks, land, landType, user=None):
        self._testAccessAdmin(user)

        for chunk in chunks:
            if chunk < 0 or chunk > 15625:
                raise exceptions.args.Arguments('Wrong coordinate')

        return super().fillChunks(chunks, land, landType, user)

    def searchUser(self, userLogin, user):
        self._testAccessAdmin(user)

        userDomain = super().searchUser(userLogin, user)

        if userDomain and userDomain.getAdmin() is True and user.getId() != userDomain.getId():
            raise exceptions.httpCodes.Page403('Can`t edit other admin')

        return userDomain
