from tests.backend.t_services.generic import Backend_Services_Generic

import service.User

class Backend_Services_UserTest(Backend_Services_Generic):
    def _getServiceAcl(self):
        return service.User.Service_User().decorate('Acl')

    def _getServiceJsonPack(self):
        return service.User.Service_User().decorate('JsonPack')

    def testUserLogin(self):
        user = self.fixture.getUser(0)
        result, domain = self._getServiceAcl().login(user.getLogin(), user._testPassword)

        self.assertTrue(result)
        self.assertEqual(domain.getLogin(), user.getLogin())

    def testUserLoginFailt(self):
        user = self.fixture.getUser(0)
        result, domain = self._getServiceAcl().login(user.getLogin(), user._testPassword)

        self.assertFalse(result)
        self.assertIsNone(domain)
