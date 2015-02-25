from tests.backend.t_controller.generic import Backend_Controller_Generic

from tests.package.db.town import Town
from tests.package.db.resource import Resource

import tests.rerun

import service.TownBuilds

import time


class Backend_Controller_MapTest(
    Backend_Controller_Generic,
    Town,
    Resource
):
    def _getCeleryController(self):
        import controller.ResourceController
        return controller.ResourceController.CeleryPrivateController()

    def _getBuildsService(self):
        return service.TownBuilds.Service_TownBuilds()

    def setUp(self):
        self.initCelery()
        super().setUp()

        self.transfer = self._login()
        self.user = self.transfer.getUser()

        self.fillTerrain(0, 0, 3, 3)
        self.town = self.addTown(0, 0, self.user, population=10000, typeTown=self.TOWN_TYPE_CITY)
        self.builds = self.town.getBuilds()

        self.addResource(0, 1, self.TYPE_RESOURCE_RUBINS, user=self.user, town=self.town, amount=100000, baseOutput=5000)
        self.addResource(0, 2, self.TYPE_RESOURCE_WOOD, user=self.user, town=self.town, amount=100000, baseOutput=5000)
        self.addResource(0, 3, self.TYPE_RESOURCE_STEEL, user=self.user, town=self.town, amount=100000, baseOutput=5000)
        self.addResource(1, 0, self.TYPE_RESOURCE_STONE, user=self.user, town=self.town, amount=100000, baseOutput=5000)
        self.addResource(1, 1, self.TYPE_RESOURCE_EAT, user=self.user, town=self.town, amount=100000, baseOutput=5000)

        self.resources = self.user.getResources()
        self.resources.setRubins(0)
        self.resources.setWood(0)
        self.resources.setStone(0)
        self.resources.setSteel(0)
        self.resources.setEat(0)
        self.resources.getMapper().save(self.resources)

    @tests.rerun.retry(5)
    def testResourcesUp(self):
        self.addTownBuild(self.town, self.TOWN_BUILD_FARM, 50) # x1.5
        self.addTownBuild(self.town, self.TOWN_BUILD_MINE, 50) # x2

        time.sleep(3)

        self.resources.extract(True)

        self.assertEqual(1000, self.resources.getWood())
        self.assertEqual(2000, self.resources.getSteel())
        self.assertEqual(2000, self.resources.getStone())
        self.assertEqual(12000, self.resources.getRubins())
        self.assertEqual(1500, self.resources.getEat())
