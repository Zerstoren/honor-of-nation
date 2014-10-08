import service.Map
import service.MapUserVisible

import exceptions.httpCodes

class Decorate():
    def getResourceByPosition(self, mapCoordinate, user=None):
        """
        :type mapCoordinate: helpers.MapCoordinate.MapCoordinate
        :type user: models.User.Domain.User_Domain
        """
        mapPosition = service.Map.Service_Map().getByPosition(mapCoordinate)

        if not service.MapUserVisible.Service_MapUserVisible().isOpen(mapPosition, user):
            raise exceptions.httpCodes.Page403('Вы не видите ресурс')


        return super().getResourceByPosition(mapCoordinate, user)
