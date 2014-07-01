from tests.selenium.PathMove import generic


class Selenium_PathMove_FromMainToTownTest(generic.Selenium_PathMove_Generic):
    def setUp(self):
        super().setUp()
        self.user = self.fixture.getUser(0)
        self.town = self._createTown(
            self._fillMapOneItem(50, 50),
            self.user
        )

        self.town.getPosition().addAccessToUser(self.user)

    def testOpenMainAndMoveToTown(self):
        self.login()

        self.assertEqual(
            '/',
            self.getUrl()
        )

        self._doubleClick(
            self._getMap(50, 50).getItem()
        )

        self.assertEqual(
            '/town/' + str(self.town.getId()),
            self.getUrl()
        )

        self._historyBack()
        self.waitForSocket()

        self.assertEqual(
            '/',
            self.getUrl()
        )
