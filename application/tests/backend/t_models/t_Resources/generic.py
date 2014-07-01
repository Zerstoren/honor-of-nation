from tests.backend.t_models import generic
from tests.data.Resources import Kit as ResourceKit


class Backend_Models_Resources_Generic(generic.Backend_Models_Generic):
    def setUp(self):
        super().setUp()

        self.map = self._fillMapOneItem(39, 39)
        self.user = self.fixture.getUser(0)
        self.town = self._createTown(
            self._fillMapOneItem(40, 40),
            self.user
        )
