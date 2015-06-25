from .Abstract import AbstractService

from service.User import Service_User
from service.Map import Service_Map
from service.MapUserVisible import Service_MapUserVisible
from service.MapResources import Service_MapResources
from service.Town import Service_Town

import exceptions.database
import exceptions.message


class Service_Admin(AbstractService.Service_Abstract):

    def fillCoordinate(self, coordinate, land, landType, user=None):
        return Service_Map().decorate(Service_Map.PARAMS).fillCoordinate(coordinate, land, landType)

    def fillChunks(self, chunks, land, landType, user=None):
        return Service_Map().decorate(Service_Map.PARAMS).fillChunks(chunks, land, landType)

    def searchUser(self, userLogin, user):
        try:
            return Service_User().searchUser(userLogin)
        except exceptions.database.NotFound:
            raise exceptions.message.Message('Пользователь с логином %s не найден' % userLogin)

    def openMapForUser(self, user, coordinate, aclUser=None):
        mapCollection = Service_Map().decorate(Service_Map.PARAMS).getRegion(coordinate)
        return Service_MapUserVisible().openRegion(user, mapCollection)

    def saveMapResources(self, user, domainData):
        return Service_MapResources().decorate(Service_MapResources.PARAMS).saveResources(domainData)

    def getTownByPosition(self, x, y):
        return Service_Town().decorate(Service_Map.PARAMS_JSONPACK).loadByPosition(x, y)

    def saveTown(self, user, townData):
        return Service_Town().decorate(Service_Town.PARAMS_JSONPACK).save(townData)

    def getAllUsers(self, user):
        return Service_User().decorate(Service_User.JSONPACK).getAllUsers()

    def decorate(self, *args):
        """
        :rtype: Service_Admin
        """
        return super().decorate(*args)
