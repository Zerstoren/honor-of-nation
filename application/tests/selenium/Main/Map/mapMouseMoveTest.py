from tests.selenium.Main.Map import generic


class Selenium_Main_Map_MapMouseMoveTest(generic.Selenium_Main_Map_Generic):
    def setUp(self):
        super().setUp()
        self.user = self.fixture.getUser(0)
        mapCollection = self._fillMap(379, self.user)
        self._createTown(mapCollection.findById(100050), self.user)

    def testMoveMap(self):
        self.login(self.user)

        mapStart = self._getMap(50, 50)
        self._moveCamera(mapStart, (90, 90))
        self._getMap(90, 90)
