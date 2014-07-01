from tests.selenium.Main import generic


class Selenium_Main_Interface_Generic(generic.Selenium_Main_Generic):
    def setUp(self):
        super().setUp()
        self.user = self.fixture.getUser(0)
        self._fillMap(379, self.user)

    def _prepareResources(self):
        self.resource1 = self._createResource(
            self._fillMapOneItem(51, 51),
            typeResource='rubins'
        )

        self.resource2 = self._createResource(
            self._fillMapOneItem(52, 51),
            typeResource='steel'
        )

        self.resource3 = self._createResource(
            self._fillMapOneItem(53, 51),
            typeResource='stone'
        )

        self.resource4 = self._createResource(
            self._fillMapOneItem(54, 51),
            typeResource='wood'
        )

        self.resource5 = self._createResource(
            self._fillMapOneItem(55, 51),
            typeResource='eat'
        )

    def _prepareTown(self):
        self.town1 = self._createTown(
            self._fillMapOneItem(50, 50),
            self.user,
            0
        )

        self.town2 = self._createTown(
            self._fillMapOneItem(51, 50),
            self.fixture.getUser(1),
            1
        )

        self.town3 = self._createTown(
            self._fillMapOneItem(52, 50),
            self.fixture.getUser(2),
            2
        )
