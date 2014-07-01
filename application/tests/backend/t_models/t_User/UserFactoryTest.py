from tests.backend.t_models.t_User import generic
from models.User import Factory


class Backend_Model_User_UserMapperTest(generic.Backend_Models_User_Generic):

    def testFetchIndexes(self):
        user = self.fixture.getUser(2)

        fetchUserId = Factory.factory.getById(user.getId())
        fetchUserLogin = Factory.factory.getByLogin(user.getLogin())

        self.assertEqual(user._getData(), fetchUserId._getData())
        self.assertEqual(user._getData(), fetchUserLogin._getData())
        self.assertEqual(fetchUserId, fetchUserLogin)

    def testFetchWithoutIndexes(self):
        user = self.fixture.getUser(2)
        Factory.factory.removeDomainFromIndex(user)

        fetchId = Factory.factory.getById(user.getId())
        Factory.factory.removeDomainFromIndex(user)

        fetchLogin = Factory.factory.getByLogin(user.getLogin())
        Factory.factory.removeDomainFromIndex(user)

        self.assertDictEqual(
            user._getData(),
            fetchId._getData()
        )

        self.assertDictEqual(
            user._getData(),
            fetchLogin._getData()
        )
