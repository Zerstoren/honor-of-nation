import service.User
import service.Map

from helpers.MapCoordinate import MapCoordinate
from helpers.mongo import objectId

class Decorate():
    def acceptBattle(self, mapCoordinate, acceptUser, info, user=None):
        mapCoordinate = MapCoordinate(posId=mapCoordinate)

        acceptUser = service.User.Service_User().getUserDomain(acceptUser)

        return super().acceptBattle(mapCoordinate, acceptUser, info, user)

    def startBattle(self, battleAskId):
        battleAskId = objectId(battleAskId)
        return super().startBattle(battleAskId)