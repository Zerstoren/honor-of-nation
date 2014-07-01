from tests.selenium.Town.Builds import generic
from models.TownsBuilds import TownsBuildDomain


class Selenium_Town_Builds_BuildsTest(generic.Selenium_Town_Build_Generic):
    def testAddBuildToQueue(self):
        self.loginToTown()

        chains = self.getChainAction()
        chains.move_to_element(
            self.byCssSelector('.build_container')
        )
        chains.perform()
        self.sleep(0.5)

        # Assert exist
        self.getPopup()

        element = self.byCssSelector('.build-queue-%s a' % TownsBuildDomain.TownsBuildDomain.BUILD_FARM)
        element.click()
        element.click()

        self.waitForSocket()

        self.assertEqual(
            'Ферма ур. 1',
            self.byCssSelector('.buildInProgress .name').text
        )

        self.sleep(5)

        self.assertEqual(
            'Ферма ур. 2',
            self.byCssSelector('.buildInProgress .name').text
        )

    def testAddBuildToQueue_BuildCompleteOnBackground(self):
        builds = self.town.getSubDomainBuilds()
        editBuilds = builds.edit()
        editBuilds.putBuildQueue(
            builds.BUILD_FARM,
            1,
            1
        )
        editBuilds.getMapper().saveQueue(editBuilds)

        self.sleep(2)
        self.loginToTown()
        self.assertElementNotExist('.alertify-log', 'css')
