from tests.backend.t_controller.generic import Backend_Controller_Generic

import service.Admin


class AbstractAdminController(Backend_Controller_Generic):
    def _getAdminService(self):
        return service.Admin.Service_Admin()


class MainAdminController(AbstractAdminController):
    def fillTerrain(self, transfer, data):
        if data['type'] == 'coordinate':
            result = self._getAdminService().fillCoordinate(
                data['coordinate'],
                data['fillLand'],
                data['fillLandType']
            )
        else:
            result = self._getAdminService().fillChunks(
                data['chunks'],
                data['fillLand'],
                data['fillLandType']
            )


        transfer.send('/admin/fillTerrain', {
            'done': result
        })

