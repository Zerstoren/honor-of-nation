import exceptions.httpCodes


class Decorate():
    def _checkAccess(self, armyUser, user):
        if armyUser.getId() != user.getId():
            raise exceptions.httpCodes.Page403('Доступ закрыт на эту страницу')

    def load(self, armyUser, position, user=None):
        self._checkAccess(armyUser, user)
        return super().load(armyUser, position, user)

    def move(self, general, path, user=None):
        pass

    def changeMoveType(self, general, move, user=None):
        pass

    def merge(self, armyCollection, user=None):
        for i in armyCollection:
            self._checkAccess(i, user)

        return super().merge(armyCollection, user)

    def split(self, armyDomain, size, user=None):
        self._checkAccess(armyDomain, user)
        return super().merge(armyDomain, size, user)

    def addSuite(self, generalArmy, solidersArmy, user=None):
        self._checkAccess(generalArmy, user)
        self._checkAccess(solidersArmy, user)
        return super().addSuite(generalArmy, solidersArmy, user)

    def removeSuite(self, generalArmy, solidersArmy, user=None):
        self._checkAccess(generalArmy, user)
        self._checkAccess(solidersArmy, user)
        return super().removeSuite(generalArmy, solidersArmy, user)

    def addSolidersToGeneral(self, generalArmy, solidersCollection, user=None):
        self._checkAccess(generalArmy, user)
        for i in solidersCollection:
            self._checkAccess(i, user)

        return super().addSolidersToGeneral(generalArmy, solidersCollection, user)

    def removeSolidersFromGeneral(self, generalArmy, solidersCollection, user=None):
        self._checkAccess(generalArmy, user)
        for i in solidersCollection:
            self._checkAccess(i, user)

        return super().removeSolidersToGeneral(generalArmy, solidersCollection, user)

    def moveInBuild(self, armyDomain, user=None):
        self._checkAccess(armyDomain, user)
        return super().moveInBuild(armyDomain, user)

    def moveOutBuild(self, armyDomain, user=None):
        self._checkAccess(armyDomain, user)
        return super().moveOutBuild(armyDomain, user)

    def dissolution(self, armyDomain, user=None):
        self._checkAccess(armyDomain, user)
        return super().dissolution(armyDomain, user)
