from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.AdminController
import exceptions.httpCodes


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
                "toX": 4,
                "toY": 4
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
            "chunks": [1],
            "fillLand": "valley",
            "fillLandType": 1,
            "type": "chunks",
        })

        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])

    def testFillTerrain_ExpectedException(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()
        user.setAdmin(False)
        user.getMapper().save(user)

        self.assertRaises(
            exceptions.httpCodes.Page403,
            controller.fillTerrain,
            transfer,
            {
                "coordinate": {
                    "fromX": 1,
                    "fromY": 1,
                    "toX": 1,
                    "toY": 1
                },
                "fillLand": "valley",
                "fillLandType": 1,
                "type": "coordinate",
            }
        )
