from tests.selenium.Main.Map import generic


class Selenium_Main_Map_ResourceTest(generic.Selenium_Main_Map_Generic):
    def setUp(self):
        super().setUp()

        self.user = self.fixture.getUser(0)

        self.map1 = self._fillMapOneItem(51, 51)
        self.map2 = self._fillMapOneItem(52, 51)
        self.map3 = self._fillMapOneItem(53, 51)
        self.map4 = self._fillMapOneItem(54, 51)
        self.map5 = self._fillMapOneItem(55, 51)

        self.map1.addAccessToUser(self.user)
        self.map2.addAccessToUser(self.user)
        self.map3.addAccessToUser(self.user)
        self.map4.addAccessToUser(self.user)
        self.map5.addAccessToUser(self.user)

        self.town = self._createTown(
            self._fillMapOneItem(50, 50),
            self.user
        )

        self.town.getPosition().addAccessToUser(self.user)

    def testViewResource(self):
        resourceRubins = self._createResource(self.map1, typeResource='rubins')
        resourceWood = self._createResource(self.map2, typeResource='wood')
        resourceSteel = self._createResource(self.map3, typeResource='steel')
        resourceStone = self._createResource(self.map4, typeResource='stone')
        resourceEat = self._createResource(self.map5, typeResource='eat')

        self.login()

        self.assertRegexpMatches(
            self._getMap(51, 51).getContainer(resourceRubins.getId()).get_attribute('innerHTML'),
            r'town_type_%s' % resourceRubins.getArmorType()
        )
        self.assertRegexpMatches(
            self._getMap(52, 51).getContainer(resourceWood.getId()).get_attribute('innerHTML'),
            r'town_type_%s' % resourceWood.getArmorType()
        )
        self.assertRegexpMatches(
            self._getMap(53, 51).getContainer(resourceSteel.getId()).get_attribute('innerHTML'),
            r'town_type_%s' % resourceSteel.getArmorType()
        )
        self.assertRegexpMatches(
            self._getMap(54, 51).getContainer(resourceStone.getId()).get_attribute('innerHTML'),
            r'town_type_%s' % resourceStone.getArmorType()
        )
        self.assertRegexpMatches(
            self._getMap(55, 51).getContainer(resourceEat.getId()).get_attribute('innerHTML'),
            r'town_type_%s' % resourceEat.getArmorType()
        )
