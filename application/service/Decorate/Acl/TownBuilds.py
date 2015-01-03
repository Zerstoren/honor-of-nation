import exceptions.httpCodes

class Decorate():
    def _userCanAccessToTownManipulation(self, user, townDomain):
        if (townDomain.getUser().getId() != user.getId()):
            raise exceptions.httpCodes.Page403('Доступ закрыт на эту страницу')

    def get(self, townDomain, user):
        self._userCanAccessToTownManipulation(user, townDomain)
        return super().get(townDomain, user)

    def create(self, user, townDomain, buildKey, level):
        self._userCanAccessToTownManipulation(user, townDomain)
        return super().create(user, townDomain, buildKey, level)

    def remove(self, user, townDomain, buildKey, level):
        self._userCanAccessToTownManipulation(user, townDomain)
        return super().remove(user, townDomain, buildKey, level)
