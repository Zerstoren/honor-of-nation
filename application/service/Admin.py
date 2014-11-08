from .Abstract import AbstractService

import service.User
import service.Map
import service.MapUserVisible
import service.MapResources
import service.Town

import exceptions.database
import exceptions.message


class Service_Admin(AbstractService.Service_Abstract):

    def fillCoordinate(self, coordinate, land, landType, user=None):
        return service.Map.Service_Map().decorate('Params').fillCoordinate(coordinate, land, landType)

    def fillChunks(self, chunks, land, landType, user=None):
        return service.Map.Service_Map().decorate('Params').fillChunks(chunks, land, landType)

    def searchUser(self, userLogin, user):
        try:
            return service.User.Service_User().searchUser(userLogin)
        except exceptions.database.NotFound:
            raise exceptions.message.Message('Пользователь с логином %s не найден' % userLogin)

    def openMapForUser(self, user, coordinate):
        mapCollection = service.Map.Service_Map().decorate('Params').getRegion(coordinate)
        return service.MapUserVisible.Service_MapUserVisible().openRegion(user, mapCollection)

    def saveMapResources(self, user, domainData):
        return service.MapResources.Service_MapResources().decorate('Params').saveResources(domainData)

    def getTownByPosition(self, x, y):
        return service.Town.Service_Town().decorate('Params', 'JsonPack').loadByPosition(x, y)

    def saveTown(self, user, townData):
        return service.Town.Service_Town().decorate('Params', 'JsonPack').save(townData)

    def getAllUsers(self, user):
        return service.User.Service_User().decorate('JsonPack').getAllUsers()

    def decorate(self, *args):
        """
        :rtype: Service_Admin
        """
        return super().decorate(*args)
