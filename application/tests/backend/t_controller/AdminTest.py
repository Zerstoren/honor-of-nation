from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.AdminController
import models.Map.Factory


class Backend_Controller_AdminTest(Backend_Controller_Generic):
    def _getModelController(self):
        return controller.AdminController.MainAdminController()

    def testFillTerrain(self):
        controller = self._getModelController()
        transfer = self._login()

        controller.fillTerrain(transfer, {
            "coordinate": {
                "fromX": 1,
                "fromY": 1,
                "toX": 32,
                "toY": 32
            },
            "fillLand": "valley",
            "fillLandType": 1,
            "type": "coordinate",
        })

        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])

    def testFillTerrainChunks(self):
        controller = self._getModelController()
        transfer = self._login()

        controller.fillTerrain(transfer, {
            "chunks": [1,2,3],
            "fillLand": "valley",
            "fillLandType": 1,
            "type": "chunks",
        })

        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])
