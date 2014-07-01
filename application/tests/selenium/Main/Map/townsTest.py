from tests.selenium.Main.Map import generic


class Selenium_Main_Map_TownsTest(generic.Selenium_Main_Map_Generic):
    def testLoadOneTown(self):
        user = self.fixture.getUser(0)
        mapCollection = self._fillMap(379)
        mapCollection.addAccessToUser(user)

        mapDomain = mapCollection.findById(100050)

        townDomain = self._createTown(mapDomain, user)
        self.login(user)
        self.waitForSocket()
        townContainer = self.byCssSelector('#container_' + str(townDomain.getId()))

        self.assertElementExist('.town_type_0', parent=townContainer)
        self.assertEqual(
            townContainer.byCss('.user_login').get_attribute('innerHTML'),
            user.getLogin()
        )

        self.assertEqual(
            townContainer.byCss('.town_name').get_attribute('innerHTML'),
            townDomain.getName()
        )

    def testLoadManyTowns(self):
        user = self.fixture.getUser(0)
        user2 = self.fixture.getUser(1)

        mapCollection = self._fillMap(379)
        mapCollection.addAccessToUser(user)
        mapCollection.addAccessToUser(user2)

        mapDomain = mapCollection.findById(100050)
        mapDomain2 = mapCollection.findById(100052)

        townDomain = self._createTown(mapDomain, user)

        townDomain2 = self._createTown(mapDomain2, user2)

        self.login(user)

        townContainer = self.byCssSelector('#container_' + str(townDomain.getId()))
        self.assertElementExist('.town_type_0', parent=townContainer)
        self.assertEqual(
            townContainer.byCss('.user_login').get_attribute('innerHTML'),
            user.getLogin()
        )

        self.assertEqual(
            townContainer.byCss('.town_name').get_attribute('innerHTML'),
            townDomain.getName()
        )

        townContainer2 = self.byCssSelector('#container_' + str(townDomain2.getId()))
        self.assertElementExist('.town_type_0', parent=townContainer2)
        self.assertEqual(
            townContainer2.byCss('.user_login').get_attribute('innerHTML'),
            user2.getLogin()
        )

        self.assertEqual(
            townContainer2.byCss('.town_name').get_attribute('innerHTML'),
            townDomain2.getName()
        )
