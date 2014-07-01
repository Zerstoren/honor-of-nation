from tests.backend.t_services.generic import Backend_Services_Generic

import service.Resources


class Backend_Services_ResourcesTest(Backend_Services_Generic):
    def _getServiceAcl(self):
        return service.Resources.Service_Resources().decorate('Acl')

    def _getServiceJsonPack(self):
        return service.Resources.Service_Resources().decorate('JsonPack')

    def testGetResources(self):
        service = self._getServiceAcl()
        resourceDomain = service.getResources(self.fixture.getUser(0))

        self.assertEqual(resourceDomain.getRubins(), 1000000)
        self.assertEqual(resourceDomain.getWood(), 1000000)
        self.assertEqual(resourceDomain.getSteel(), 1000000)
        self.assertEqual(resourceDomain.getEat(), 1000000)
        self.assertEqual(resourceDomain.getStone(), 1000000)
        self.assertEqual(resourceDomain.getUser(), self.fixture.getUser(0))
