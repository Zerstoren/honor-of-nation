from tests.backend.t_models.t_User import generic
from models.User import Factory


class Backend_Model_User_UserDomainTest(generic.Backend_Models_User_Generic):

    def testUserAdd(self):
        # Create data
        domain, edit = Factory.factory.createUser()
        edit.setLogin("Rand")
        edit.setNewPassword("123456")
        edit.setPosition(x=0, y=0)
        Factory.factory.add(edit)

        self.assertDictEqual(
            domain._getData(),
            self._getFromBaseUser(domain)
        )

        # Load from index
        userLoaded = Factory.factory.getByLogin('Rand')

        # Check loaded data
        self.assertDictEqual(
            domain._getData(),
            self._getFromBaseUser(userLoaded)
        )

        # Check working index
        self.assertEqual(
            userLoaded,
            domain
        )

        edit = domain.edit()
        edit.setLogin('Bulk')
        Factory.factory.save(edit)

        userLoaded = Factory.factory.getByLogin('Bulk')
        self.assertEqual(
            userLoaded,
            domain
        )

        Factory.factory.removeDomainFromIndex(domain)

    def testUserEdit(self):
        user = self.fixture.getUser(3)

        writer = user.edit()
        writer.setLogin('Other')
        writer.setPosition(x=25, y=25)
        writer.setNewPassword('ast')

        Factory.factory.save(writer)

        self.assertEqual(user.getLogin(), 'Other')
        self.assertDictEqual(user.getPosition(), {"x": 25, "y": 25})

        self.assertDictEqual(
            self._getFromBaseUser(user),
            user._getData()
        )

    def testUserDecorateResource(self):
        user = self.fixture.getUser(3)
        resource = user.getSubDomainResource()
        self.assertEqual(
            resource.getResources(),
            {
                resource.RESOURCE_RUBINS: 0,
                resource.RESOURCE_WOOD: 0,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_STEEL: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 0
            }
        )

        ### Up resource
        edit = resource.edit()
        edit.upResource(resource.RESOURCE_RUBINS, 200)
        edit.upResource(resource.RESOURCE_WOOD, 2)
        edit.upResource(resource.RESOURCE_GOLD, 20)
        edit.getMapper().save(edit)

        self.assertEqual(
            resource.getResources(),
            {
                resource.RESOURCE_RUBINS: 200,
                resource.RESOURCE_WOOD: 2,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_STEEL: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 20
            }
        )

        ### down resource
        edit = resource.edit()
        edit.downResource(resource.RESOURCE_RUBINS, 100)
        edit.downResource(resource.RESOURCE_WOOD, 1)
        edit.downResource(resource.RESOURCE_GOLD, 10)
        edit.getMapper().save(edit)

        self.assertEqual(
            resource.getResources(),
            {
                resource.RESOURCE_RUBINS: 100,
                resource.RESOURCE_WOOD: 1,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_STEEL: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 10
            }
        )
