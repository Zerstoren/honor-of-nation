from tests.selenium.Admin import generic

class Selenium_Admin_TerrainTest(generic.Selenium_Admin_Generic):
    def testCreateTerrainByCoordinate(self):
        self.login()
        self.sleep(10)