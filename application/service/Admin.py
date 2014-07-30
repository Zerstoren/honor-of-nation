from .Abstract import AbstractService
import models.Map.Mapper
import models.Map.Math
import models.Map.Factory
import models.Map.Domain

import exceptions.database

import service.User
import service.Map
import service.MapUserVisible

import config


class Service_Admin(AbstractService.Service_Abstract):

    def fillCoordinate(self, coordinate, land, landType, user=None):
        return service.Map.Service_Map().fillCoordinate(coordinate, land, landType)

    def fillChunks(self, chunks, land, landType, user=None):
        return service.Map.Service_Map().fillChunks(chunks, land, landType)

    def searchUser(self, userLogin, user):
        return service.User.Service_User().searchUser(userLogin)

    def openMapForUser(self, user, coordinate):
        mapCollection = service.Map.Service_Map().getRegion(
            fromX=coordinate['fromX'],
            fromY=coordinate['fromY'],
            toX=coordinate['toX'],
            toY=coordinate['toY']
        )
        return service.MapUserVisible.Service_MapUserVisible().openRegion(user, mapCollection)

    def decorate(self, *args):
        """
        :rtype: Service_Admin
        """
        return super().decorate(*args)