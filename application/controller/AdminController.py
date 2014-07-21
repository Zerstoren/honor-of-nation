from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.ResourceController

import service.Admin
import service.Resources

import exceptions.httpCodes
import exceptions.database


class AbstractAdminController(Backend_Controller_Generic):
    def _getAclAdminService(self):
        return service.Admin.Service_Admin().decorate('Acl')

    def _getJsonPackAclAdminService(self):
        return service.Admin.Service_Admin().decorate('JsonPack', 'Acl')

    def _getJsonPackResourceService(self):
        return service.Resources.Service_Resources().decorate('JsonPack')


class MainAdminController(AbstractAdminController):
    def fillTerrain(self, transfer, data):

        if data['type'] == 'coordinate':
            result = self._getAclAdminService().fillCoordinate(
                data['coordinate'],
                data['fillLand'],
                data['fillLandType'],
                transfer.getUser()
            )
        else:
            result = self._getAclAdminService().fillChunks(
                data['chunks'],
                data['fillLand'],
                data['fillLandType'],
                transfer.getUser()
            )

        transfer.send('/admin/fillTerrain', {
            'done': result
        })

    def searchUser(self, transfer, data):
        try:
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

        except exceptions.httpCodes.Page403 as e:
            transfer.send('/admin/searchUser', {
                'done': False,
                'error': str(e)
            })

        except exceptions.database.NotFound:
            transfer.send('/admin/searchUser', {
                'done': False,
                'error': 'User with login %s not found' % data['login']
            })

    def saveResources(self, transfer, data):
        try:
            user = self._getAclAdminService().searchUser(data['userLogin'], transfer.getUser())
            service.Resources.Service_Resources().setResources(user, data['resources'])
            transfer.send('/admin/searchUser', {
                'done': True
            })

            controller.ResourceController.DeliveryController().resourceChange(user)

        except exceptions.httpCodes.Page403 as e:
            transfer.send('/admin/searchUser', {
                'done': False,
                'error': str(e)
            })

        except exceptions.database.NotFound:
            transfer.send('/admin/searchUser', {
                'done': False,
                'error': 'User with login %s not found' % data['login']
            })
