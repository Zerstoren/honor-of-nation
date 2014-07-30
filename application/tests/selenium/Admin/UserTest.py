from tests.selenium.Admin import generic

class Selenium_Admin_TerrainTest(generic.Selenium_Admin_Generic):
    def _setResource(self, name, value):
        self.byCssSelector('.resources-edit input.' + name).clear()
        self.byCssSelector('.resources-edit input.' + name).send_keys(value)

    def testCreateTerrainByCoordinate(self):
        user = self.login()
        self._goToAdmin()

        self.byAttribute('data-type', 'player').click()
        self.byCssSelector('.search-user-login').send_keys(user.getLogin())
        self.byCssSelector('.search-user').click()

        self.waitForElement('.resources-edit')

        self._setResource('rubins', 5)
        self._setResource('wood', 10)
        self._setResource('steel', 50)
        self._setResource('stone', 100)
        self._setResource('eat', 200)
        self._setResource('gold', 500)

        self.byCssSelector('.save-info').click()

        self.operationIsSuccess()

    def testCreateTerrainByCoordinate_WrongUser(self):
        self.login()
        self._goToAdmin()

        self.byAttribute('data-type', 'player').click()
        self.byCssSelector('.search-user-login').send_keys(self.fixture.getUser(1).getLogin())
        self.byCssSelector('.search-user').click()

        self.operationIsFail()

    def testOpenMapForUser(self):
        self.fillTerrain(0, 0, 4, 4)

        self.login()
        self._goToAdmin()
        self.byAttribute('data-type', 'player').click()

        self.byCssSelector('div.from .x').send_keys(0)
        self.byCssSelector('div.from .y').send_keys(0)

        self.byCssSelector('div.to .x').send_keys(4)
        self.byCssSelector('div.to .y').send_keys(4)

        self.byCssSelector('.save-coordinate').click()

        self.operationIsSuccess()