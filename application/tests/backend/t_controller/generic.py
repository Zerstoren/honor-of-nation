from tests.backend import generic
from models.User.Domain import User_Domain


class Backend_Controller_Generic(generic.Backend_Generic):
    def _login(self, user=None):
        """
        :rtype: tests.mock.Transfer.TransferMock
        """
        assert isinstance(user, User_Domain) or user is None

        if user is None:
            user = self.fixture.getUser(0)

        if not user.hasTransfer():
            transfer = self.mockLoad('Transfer', user)
        else:
            transfer = user.getTransfer()

        return transfer
