import exceptions.httpCodes

class Decorate():
    def get(self, townDomain, user):
        if (townDomain.getUser().getId() != user.getId()):
            exceptions.httpCodes.Page403('Доступ закрыт на эту страницу')

        return super().get(townDomain, user)
