import exceptions.httpCodes


class Decorate():
    def testUser(self, userAction, userSend):
        if userAction.getId() != userSend.getId():
            raise exceptions.httpCodes.Page403('Доступ закрыт на эту страницу')

    def acceptBattle(self, mapCoordinate, acceptUser, info, user=None):
        self.testUser(acceptUser, user)

        return super().acceptBattle(mapCoordinate, acceptUser, info, user)
