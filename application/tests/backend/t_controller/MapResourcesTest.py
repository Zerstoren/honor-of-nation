from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.MapResourcesController

import exceptions.httpCodes

from tests.package.db.resource import Resource
from tests.package.db.town import Town

import time


class Backend_Controller_MapResources(
    Backend_Controller_Generic,
    Resource
):
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

class Backend_Controller_MapCeleryResources(
    Backend_Controller_Generic,
    Town,
    Resource
):
    def setUp(self):
        self.initCelery()
        super().setUp()

        self.transfer = self._login()
        self.user = self.transfer.getUser()

        self.fillTerrain(0, 0, 3, 3)
        self.town = self.addTown(0, 0, self.user, population=10000, typeTown=self.TOWN_TYPE_CITY)
        self.builds = self.town.getBuilds()

        self.rubins = self.addResource(0, 1, self.TYPE_RESOURCE_RUBINS, user=self.user, town=self.town, amount=10000, baseOutput=5000)
        self.wood = self.addResource(0, 2, self.TYPE_RESOURCE_WOOD, user=self.user, town=self.town, amount=10000, baseOutput=5000)
        self.steel = self.addResource(0, 3, self.TYPE_RESOURCE_STEEL, user=self.user, town=self.town, amount=10000, baseOutput=5000)
        self.stone = self.addResource(1, 0, self.TYPE_RESOURCE_STONE, user=self.user, town=self.town, amount=10000, baseOutput=5000)
        self.eat = self.addResource(1, 1, self.TYPE_RESOURCE_EAT, user=self.user, town=self.town, amount=10000, baseOutput=5000)


    def testResourcesDown(self):
        self.addTownBuild(self.town, self.TOWN_BUILD_FARM, 50)

        time.sleep(6)

        self.rubins.extract(True)
        self.assertEqual(5000, self.rubins.getAmount())

        self.wood.extract(True)
        self.assertEqual(5000, self.wood.getAmount())

        self.steel.extract(True)
        self.assertEqual(5000, self.steel.getAmount())

        self.stone.extract(True)
        self.assertEqual(5000, self.stone.getAmount())

        self.eat.extract(True)
        self.assertEqual(2500, self.eat.getAmount())
