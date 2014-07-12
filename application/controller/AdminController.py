from tests.backend.t_controller.generic import Backend_Controller_Generic

import service.Admin


class AbstractAdminController(Backend_Controller_Generic):
    def _getAclAdminService(self):
        return service.Admin.Service_Admin().decorate('Acl')


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

