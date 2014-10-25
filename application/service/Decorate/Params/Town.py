import service.User
import helpers.mongo
import helpers.MapCoordinate

class Decorate():
    def getById(self, townId):
        return super().getById(
            helpers.mongo.objectId(townId)
        )

    def loadByPosition(self, x, y):
        return super().loadByPosition(
            helpers.MapCoordinate.MapCoordinate(x=x, y=y)
        )

    def save(self, townData):
        townData['type'] = int(townData['type'])
        townData['population'] = int(townData['population'])
        townData['pos_id'] = int(townData['pos_id'])
        townData['user'] = service.User.Service_User().getUserDomain(
            helpers.mongo.objectId(townData['user'])
        )

        return super().save(townData)