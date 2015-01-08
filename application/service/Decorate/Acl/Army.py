import exceptions.httpCodes
"""
Access Layer Level for decorate base service class
"""
class Decorate():
    def _checkAccess(self, armyUser, user):
        if armyUser.getId() != user.getId():
            raise exceptions.httpCodes.Page403('Доступ закрыт на эту страницу')

    def load(self, armyUser, position, user=None):
        self._checkAccess(armyUser, user)
        return super().load(armyUser, position, user)
