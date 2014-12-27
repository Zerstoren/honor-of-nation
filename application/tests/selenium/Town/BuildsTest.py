from tests.selenium.Town import generic
from models.TownBuilds import Common as buildConst
import tests.rerun

from tests.package.asserts import Asserts

from tests.package.db.town import Town

class Selenium_Town_BuildsTest(
    generic.Selenium_Town_Generic,
    Asserts,
    Town
):
    def setUp(self):
        super().setUp()

        self.user = self.fixture.getUser(0)

        self.fillTerrain(0, 0, 2, 2)
        self.town = self.addTown(1, 1, self.user, 10000)
        self.builds = self.town.getBuilds()

        self.resources = self.user.getResources()
        self.resources.setRubins(1000000)
        self.resources.setWood(1000000)
        self.resources.setStone(1000000)
        self.resources.setSteel(1000000)
        self.resources.setEat(1000000)
        self.resources.getMapper().save(self.resources)

        self.login()
        self.openTown(self.town)

    @tests.rerun.retry()
    def testBaseCreateAndRemove(self):
        self._getBuildElement(buildConst.BUILD_V_COUNCIL).click()

        self.waitForSocket()

        self.assertEqual(
            self._getCurrentBuildName(),
            'Сель. Совет'
        )

        self.assertEqual(
            self._getCurrentBuildLevel(),
            '1'
        )

        self._getCurrentBuild().byCss('.cancel').click()

        self.waitForSocket()

        self.assertElementExist(
            self._getSelectorBuild() + ' .nothing-builds'
        )
