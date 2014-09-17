import models.Map.Region


class Decorate():
    def getByPosIds(self, posIds):
        return super().getByPosIds(
            [int(i) for i in posIds]
        )

    def getRegion(self, coordinate):
        return super().getRegion(
            models.Map.Region.MapRegion(**coordinate)
        )

    def fillCoordinate(self, coordinate, land, landType):
        land = int(land)
        landType = int(landType)
        regionMap = models.Map.Region.MapRegion(**coordinate)

        return super().fillCoordinate(regionMap, land, landType)

    def fillChunks(self, chunks, land, landType):
        land = int(land)
        landType = int(landType)
        chunks = [int(i) for i in chunks]

        return super().fillChunks(chunks, land, landType)
