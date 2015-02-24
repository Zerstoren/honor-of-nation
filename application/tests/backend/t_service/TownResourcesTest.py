from tests.backend.t_service.generic import Backend_Service_Generic
from tests.package.db.town import Town
from tests.package.db.resource import Resource

import service.TownBonus
import service.TownResources

class Backend_Service_TownResources(
    Backend_Service_Generic,
    Town,
    Resource
):
    def setUp(self):
        super().setUp()
        self.user = self.fixture.getUser(0)
        self.fillTerrain(0,0,3,3)

    def testTownResources(self):
        town = self.addTown(0, 0, self.user, 10000, 1)
        self.addResource(0, 1, self.TYPE_RESOURCE_EAT, user=self.user, town=town, amount=50000, baseOutput=5000)
        self.addResource(0, 2, self.TYPE_RESOURCE_EAT, user=self.user, town=town, amount=50000, baseOutput=5000)
        self.addResource(0, 3, self.TYPE_RESOURCE_EAT, user=self.user, town=town, amount=50000, baseOutput=10000)

        self.addResource(1, 0, self.TYPE_RESOURCE_RUBINS, user=self.user, town=town, amount=50000, baseOutput=5000)
        self.addResource(1, 1, self.TYPE_RESOURCE_RUBINS, user=self.user, town=town, amount=50000, baseOutput=15000)

        self.addResource(1, 2, self.TYPE_RESOURCE_WOOD, user=self.user, town=town, amount=50000, baseOutput=10000)

        self.addResource(1, 3, self.TYPE_RESOURCE_STONE, user=self.user, town=town, amount=50000, baseOutput=10000)

        self.addResource(2, 1, self.TYPE_RESOURCE_STEEL, user=self.user, town=town, amount=50000, baseOutput=10000)

        bonusService = service.TownBonus.Service_TownBonus()
        townResourcesService = service.TownResources.Service_TownResources()

        townBuildsDomain = town.getBuilds()
        townBuildsDomain.setGuildhall(10)
        townBuildsDomain.setTCouncil(35)
        townBuildsDomain.setMill(50)
        townBuildsDomain.setField(50)
        townBuildsDomain.setFarm(50)
        townBuildsDomain.setStorage(20)
        townBuildsDomain.setRoad(40)
        townBuildsDomain.getMapper().save(townBuildsDomain)

        bonusService.recalculate(town.getBonus())

        townResourcesDomain = town.getResourcesUp()
        townResourcesService.recalculate(townResourcesDomain)

        townResourcesDomain.extract(force=True)

        # Tax, 10 000 people * (5 city tax + (0.05 * 35 tax town council) + (0.2 * 10 tax guildhall)) =
        self.assertEqual(87500, townResourcesDomain.getTax())
        # Minerals update at 5% from road (0.125 * 40)
        self.assertEqual(21000, townResourcesDomain.getRubins())
        self.assertEqual(10500, townResourcesDomain.getSteel())
        self.assertEqual(10500, townResourcesDomain.getStone())

        # No upgrades
        self.assertEqual(10000, townResourcesDomain.getWood())

        # Eat: (Mill 0.5 * 50) + (Field 0.5 * 50) + (Farm 1 * 50) + (Storage 0.5 * 20) + (Road 0.125 * 40) = 115%
        self.assertEqual(43000, townResourcesDomain.getEat())

