from helpers.MapCoordinate import MapCoordinate


class Decorate():
    def getUsersWhoSeePosition(self, posId):
        mapCoordinate = MapCoordinate(posId=posId)
        return super().getUsersWhoSeePosition(mapCoordinate)

    def getByChunks(self, user, chunks):
        return super().getByChunks(
            user,
            [int(i) for i in chunks]
        )

    def getByIds(self, user, ids):
        return super().getByIds(
            user,
            [int(i) for i in ids]
        )