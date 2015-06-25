import service.Abstract.AbstractService

import service.Map

import models.MapUserVisible.Mapper
import models.MapUserVisible.Factory


class Service_MapUserVisible(service.Abstract.AbstractService.Service_Abstract):

    def openRegion(self, user, region):
        """
        :type user:   models.User.Domain.User_Domain
        :type region: collection.MapCollection.Map_Collection
        """
        models.MapUserVisible.Mapper.MapUserVisible_Mapper.insertCollection(user, region)
        return region.getMapVisible(user)

    def isOpen(self, mapDomain, userDomain):
        """
        :type mapDomain: models.Map.Domain.Map_Domain
        :type userDomain: models.User.Domain.User_Domain
        """
        try:
            models.MapUserVisible.Factory.MapUserVisible_Factory.getVisibleDomain(
                mapDomain,
                userDomain
            )

            return True
        except:
            return False

    def openAroundPlace(self, user, mapCoordinate, aroundSize):
        from helpers.MapRegion import MapRegion

        startFromX = mapCoordinate.getX() - aroundSize
        startFromY = mapCoordinate.getY() - aroundSize
        completeToX = mapCoordinate.getX() + aroundSize
        completeToY = mapCoordinate.getY() + aroundSize

        if startFromX < 0: startFromX = 0
        if startFromY < 0: startFromY = 0
        if completeToX > 1999: completeToX = 1999
        if completeToY > 1999: completeToY = 1999

        region = MapRegion(startFromX, completeToX, startFromY, completeToY)
        mapCollection = region.getCollection()
        self.openRegion(user, mapCollection)

        import controller.MapController
        controller.MapController.DeliveryController().openRegion(user, mapCollection)

    def getByChunks(self, user, chunks):
        return models.MapUserVisible.Factory.MapUserVisible_Factory.getByChunks(user, chunks)

    def getByIds(self, user, ids):
        """
        :rtype: collection.MapUserVisibleCollection.MapUserVisible_Collection
        """
        return models.MapUserVisible.Factory.MapUserVisible_Factory.getByIds(user, ids)

    def getUsersWhoSeePosition(self, mapCoordinate):
        return models.MapUserVisible.Factory.MapUserVisible_Factory.getUsersByPosition(mapCoordinate)

    def decorate(self, *args):
        """
        :rtype: Service_MapUserVisible
        """
        return super().decorate(*args)
