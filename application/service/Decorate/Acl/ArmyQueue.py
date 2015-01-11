import exceptions.httpCodes
"""
Access Layer Level for decorate base service class
"""
class Decorate():
    def _checkAccess(self, town, user):
        if town.getUser().getId() != user.getId():
            raise exceptions.httpCodes.Page403('Доступ закрыт на эту страницу')

    def add(self, town, unit, count, user=None):
        self._checkAccess(town, user)
        return super().add(town, unit, count, user)

    def remove(self, town, queueDomain, user):
        self._checkAccess(town, user)
        return super().remove(town, queueDomain, user)

    def getQueue(self, town, user=None):
        self._checkAccess(town, user)
        return super().getQueue(town, user)
