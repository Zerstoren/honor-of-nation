from .Abstract import AbstractService

import service.User
import service.Map
import service.MapUserVisible


class Service_Admin(AbstractService.Service_Abstract):

    def fillCoordinate(self, coordinate, land, landType, user=None):
        return service.Map.Service_Map().fillCoordinate(coordinate, land, landType)

    def fillChunks(self, chunks, land, landType, user=None):
        return service.Map.Service_Map().fillChunks(chunks, land, landType)

    def searchUser(self, userLogin, user):
        return service.User.Service_User().searchUser(userLogin)

    def openMapForUser(self, user, coordinate):
        mapCollection = service.Map.Service_Map().getRegion(**coordinate)
        return service.MapUserVisible.Service_MapUserVisible().openRegion(user, mapCollection)

    def decorate(self, *args):
        """
        :rtype: Service_Admin
        """
        return super().decorate(*args)