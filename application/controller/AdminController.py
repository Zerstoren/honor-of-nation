import controller.ResourceController

import service.Admin
import service.Resources
import service.User
import service.MapResources

import exceptions.httpCodes
import exceptions.database
import exceptions.args


class AbstractAdminController():
    def _getAclAdminService(self):
        return service.Admin.Service_Admin().decorate('Acl')

    def _getAclParamsAdminService(self):
        return service.Admin.Service_Admin().decorate('Acl', 'Params')

    def _getJsonPackAclAdminService(self):
        return service.Admin.Service_Admin().decorate('JsonPack', 'Acl')

    def _getJsonPackResourceService(self):
        return service.Resources.Service_Resources().decorate('JsonPack')

    def _getJsonPackUserService(self):
        return service.User.Service_User().decorate('JsonPack')

    def _getJsonPackParamsMapResourcesService(self):
        return service.MapResources.Service_MapResources().decorate('JsonPack', 'Params')

    def _getParamsAclMapResourcesService(self):
        return service.MapResources.Service_MapResources().decorate('Params', 'Acl')


class MainAdminController(AbstractAdminController):
    def fillTerrain(self, transfer, data):

        if data['type'] == 'coordinate':
            result = self._getAclParamsAdminService().fillCoordinate(
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
        resources = self._getJsonPackResourceService().getResources(user, user)

        transfer.send('/admin/searchUser', {
            'done': True,
            'user': {
                '_id'  : str(user.getId()),
                'login': user.getLogin(),
                'admin': user.getAdmin()
            },
            'resources': resources
        })

    def saveResources(self, transfer, data):
        try:
            user = self._getAclAdminService().searchUser(data['userLogin'], transfer.getUser())
            service.Resources.Service_Resources().setResources(user, data['resources'])
            transfer.send('/admin/searchUser', {
                'done': True
            })

            controller.ResourceController.DeliveryController().resourceChange(user)

        except exceptions.database.NotFound:
            transfer.send('/admin/searchUser', {
                'done': False,
                'error': 'User with login %s not found' % data['login']
            })

    def saveCoordinate(self, transfer, data):
        try:
            user = transfer.getUser()
            self._getAclAdminService().openMapForUser(user, data)

            transfer.send('/admin/saveCoordinate', {
                'done': True
            })
        except Exception as e:
            transfer.send('/admin/saveCoordinate', {
                'done': False,
                'error': str(e)
            })

    def loadResourceMap(self, transfer, data):
        result = {}

        result['users'] = self._getJsonPackUserService().getAllUsers()

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
        result = {}
        result['done'] = self._getParamsAclMapResourcesService().saveResources(data['domain'])

        transfer.send('/admin/saveResourceDomain', result)
