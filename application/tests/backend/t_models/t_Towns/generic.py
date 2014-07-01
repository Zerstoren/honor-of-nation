from tests.backend.t_models import generic


class Backend_Models_Towns_Generic(generic.Backend_Models_Generic):
    def setUp(self):
        super().setUp()

        self.user = self.fixture.getUser(0)
        self.mapDomain = self._fillMapOneItem(40, 40)
