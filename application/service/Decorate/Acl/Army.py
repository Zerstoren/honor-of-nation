import exceptions.httpCodes


class Decorate():
    def _checkAccess(self, armyUser, user):
        if armyUser.getId() != user.getId():
            raise exceptions.httpCodes.Page403('Доступ закрыт на эту страницу')

    def load(self, armyUser, position, config=None, user=None):
        self._checkAccess(armyUser, user)
        return super().load(armyUser, position, config=config, user=user)

    def loadDetail(self, armyUser, _id, user=None):
        self._checkAccess(armyUser, user)
        return super().loadDetail(armyUser, _id, user)

    def move(self, general, mapCoordinate, user=None):
        self._checkAccess(general.getUser(), user)
        return super().move(general, mapCoordinate, user)

    def changeMoveType(self, general, move, user=None):
        pass

    def merge(self, armyCollection, user=None):
        for i in armyCollection:
            self._checkAccess(i.getUser(), user)

        return super().merge(armyCollection, user)

    def split(self, armyDomain, size, user=None):
        self._checkAccess(armyDomain.getUser(), user)
        return super().split(armyDomain, size, user)

    def addSuite(self, generalArmy, solidersArmy, user=None):
        self._checkAccess(generalArmy.getUser(), user)
        self._checkAccess(solidersArmy.getUser(), user)
        return super().addSuite(generalArmy, solidersArmy, user)

    def removeSuite(self, generalArmy, solidersArmy, user=None):
        self._checkAccess(generalArmy.getUser(), user)
        self._checkAccess(solidersArmy.getUser(), user)
        return super().removeSuite(generalArmy, solidersArmy, user)

    def addSolidersToGeneral(self, generalArmy, solidersCollection, user=None):
        self._checkAccess(generalArmy.getUser(), user)
        for i in solidersCollection:
            self._checkAccess(i.getUser(), user)

        return super().addSolidersToGeneral(generalArmy, solidersCollection, user)

    def removeSolidersFromGeneral(self, generalArmy, solidersCollection, user=None):
        self._checkAccess(generalArmy.getUser(), user)
        for i in solidersCollection:
            self._checkAccess(i.getUser(), user)

        return super().removeSolidersFromGeneral(generalArmy, solidersCollection, user)

    def moveInBuild(self, armyDomain, user=None):
        self._checkAccess(armyDomain.getUser(), user)
        return super().moveInBuild(armyDomain, user)

    def moveOutBuild(self, armyDomain, user=None):
        self._checkAccess(armyDomain.getUser(), user)
        return super().moveOutBuild(armyDomain, user)

    def dissolution(self, armyDomain, user=None):
        self._checkAccess(armyDomain.getUser(), user)
        return super().dissolution(armyDomain, user)
