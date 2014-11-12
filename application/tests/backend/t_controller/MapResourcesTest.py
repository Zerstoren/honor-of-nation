from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.MapResourcesController

import exceptions.httpCodes


class Backend_Controller_MapResources(Backend_Controller_Generic):
    def _getModelController(self):
        return controller.MapResourcesController.ModelController()

    def testModelGet(self):
        controller = self._getModelController()
        transfer = self._login()

        mapCollection = self.fillTerrain(0, 0, 2, 2)
        self.addResource(1, 1, 'rubins')
        self.openRegion(transfer.getUser(), mapCollection)

        controller.get(transfer, {
            'posId': 2001
        })

        result = transfer.getLastMessage()

        self.assertEqual(result['module'], '/model/map_resources/get')
        self.assertEqual(result['message']['done'], True)

    def testModelGet_ResourceNotVisible(self):
        controller = self._getModelController()
        transfer = self._login()

        self.fillTerrain(0, 0, 2, 2)
        self.addResource(1, 1, 'rubins')


        self.assertRaises(
            exceptions.httpCodes.Page403,
            controller.get,
            transfer,
            {
                'posId': 2001
            }
        )
