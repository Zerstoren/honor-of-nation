import controller.ResourceController

from service.Admin import Service_Admin
from service.Resources import Service_Resources
from service.MapResources import Service_MapResources

import exceptions.httpCodes
import exceptions.database
import exceptions.args


class AbstractAdminController():
    def _getAclAdminService(self):
        return Service_Admin().decorate(Service_Admin.ACL)

    def _getAdminService(self):
        return Service_Admin()

    def _getAclParamsAdminService(self):
        return Service_Admin().decorate(Service_Admin.PARAMS_ACL)

    def _getJsonPackResourceService(self):
        return Service_Resources().decorate(Service_Resources.JSONPACK)

    def _getJsonPackParamsMapResourcesService(self):
        return Service_MapResources().decorate(Service_MapResources.PARAMS_JSONPACK)


class MainAdminController(AbstractAdminController):
    def fillTerrain(self, transfer, data):
        if data['type'] == 'coordinate':
            result = self._getAclAdminService().fillCoordinate(
                data['coordinate'],
                data['fillLand'],
                data['fillLandType'],
                transfer.getUser()
            )
        elif data['type'] == 'chunks':
            result = self._getAclAdminService().fillChunks(
                data['chunks'],
                data['fillLand'],
                data['fillLandType'],
                transfer.getUser()
            )
        else:
            transfer.send('/admin/fillTerrain', {
                'done': False,
                'error': 'Переданы неверные параметры заполнения территории'
            })

            return

        transfer.send('/admin/fillTerrain', {
            'done': result
        })

    def searchUser(self, transfer, data):
        user = self._getAclAdminService().searchUser(data['login'], transfer.getUser())
        resources = self._getJsonPackResourceService().getResources(user)

        transfer.send('/admin/searchUser', {
            'done': True,
            'user': {
                '_id' : str(user.getId()),
                'login': user.getLogin(),
                'admin': user.getAdmin()
            },
            'resources': resources
        })

    def saveResources(self, transfer, data):
        user = self._getAclAdminService().searchUser(data['userLogin'], transfer.getUser())
        Service_Resources().decorate(Service_Resources.PARAMS).setResources(user, data['resources'])
        transfer.send('/admin/searchUser', {
            'done': True
        })

        controller.ResourceController.DeliveryController().resourceChange(user)

    def saveCoordinate(self, transfer, data):
        user = transfer.getUser()

        self._getAclParamsAdminService().openMapForUser(data['user'], data['coordinate'], user)

        transfer.send('/admin/saveCoordinate', {
            'done': True
        })

    def loadResourceMap(self, transfer, data):
        result = {
            'users': self._getAclAdminService().getAllUsers(transfer.getUser())
        }

        if 'x' in data and 'y' in data and data['x'] is not False and data['y'] is not False:
            try:
                result['resource'] = self._getJsonPackParamsMapResourcesService().getResourceByPosition(
                    data['x'],
                    data['y']
                )
            except exceptions.database.NotFound:
                result['resource'] = False
        else:
            result['resource'] = False

        result['done'] = True

        transfer.send('/admin/loadResourceMap', result)

    def saveResourceDomain(self, transfer, data):
        result = {
            'done': self._getAclAdminService().saveMapResources(transfer.getUser(), data['domain'])
        }

        transfer.send('/admin/saveResourceDomain', result)

    def loadTownMap(self, transfer, data):
        result = {
            'users': self._getAclAdminService().getAllUsers(transfer.getUser())
        }

        if 'x' in data and 'y' in data and data['x'] is not False and data['y'] is not False:
            result['town'] = False
            try:
                result['town'] = self._getAdminService().getTownByPosition(
                    data['x'],
                    data['y']
                )
                result['done'] = True
            except exceptions.database.NotFound:
                result['done'] = False
        else:
            result['done'] = True

        transfer.send('/admin/loadTownMap', result)

    def saveTownDomain(self, transfer, data):
        result = {
            'town': self._getAclAdminService().saveTown(transfer.getUser(), data['domain']),
            'done': True
        }

        transfer.send('/admin/saveTownDomain', result)
