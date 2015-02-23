from tests.backend.t_service.generic import Backend_Service_Generic
from tests.package.db.town import Town

import service.TownBonus

class Backend_Service_TownBonus(
    Backend_Service_Generic,
    Town
):
    def setUp(self):
        super().setUp()
        self.user = self.fixture.getUser(0)
        self.fillTerrain(0,0,1,1)

    def testTownBonus(self):
        town = self.addTown(0, 0, self.user, 10000, 1)
        bonusService = service.TownBonus.Service_TownBonus()

        townBuildsDomain = town.getBuilds()
        townBuildsDomain.setGuildhall(10)
        townBuildsDomain.setTCouncil(35)
        townBuildsDomain.setMill(50)
        townBuildsDomain.setField(50)
        townBuildsDomain.setFarm(50)
        townBuildsDomain.setStorage(20)
        townBuildsDomain.getMapper().save(townBuildsDomain)

        bonusDomain = bonusService.get(town)
        bonusService.recalculate(bonusDomain)
        bonusDomain.extract(force=True)

        self.assertEqual(35, bonusDomain.getRiot())
        self.assertEqual(35, bonusDomain.getBuildsSpeed())
        self.assertEqual(110, bonusDomain.getEat())
        self.assertEqual(3.75, bonusDomain.getTax())


