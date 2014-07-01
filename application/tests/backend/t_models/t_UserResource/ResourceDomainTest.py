from tests.backend.t_models.t_UserResource import generic
from models.UserResource import Exceptions as UserResourceExceptions

from models.UserResource import Mapper


class Backend_Models_Resource_ResourceDomainTest(generic.Backend_Models_Resource_Generic):
    def testResource_Get(self):
        user = self.fixture.getUser(0)
        resource = user.getSubDomainResource()

        res = resource.getResources()
        self.assertEqual(
            res,
            {
                resource.RESOURCE_RUBINS: 0,
                resource.RESOURCE_WOOD: 0,
                resource.RESOURCE_STEEL: 0,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 0
            }
        )

    def testResource_Set_AfterGet(self):
        user = self.fixture.getUser(0)
        resource = user.getSubDomainResource()

        edit = resource.edit()
        edit.setResource(resource.RESOURCE_RUBINS, 1200)
        edit.setResource(resource.RESOURCE_STEEL, 12000)
        edit.setResource(resource.RESOURCE_GOLD, 25.3)

        Mapper.mapper.save(edit)

        res = resource.getResources()
        self.assertEqual(
            res,
            {
                resource.RESOURCE_RUBINS: 1200,
                resource.RESOURCE_WOOD: 0,
                resource.RESOURCE_STEEL: 12000,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 25.3
            }
        )

    def testResource_Down_AfterGet(self):
        user = self.fixture.getUser(0)
        resource = user.getSubDomainResource()

        edit = resource.edit()
        edit.setResource(resource.RESOURCE_RUBINS, 12000)
        edit.setResource(resource.RESOURCE_STEEL, 12000)
        edit.setResource(resource.RESOURCE_GOLD, 25)
        Mapper.mapper.save(edit)

        edit = resource.edit()

        self.assertRaises(
            UserResourceExceptions.NotEnoughResource,
            edit.downResource,
            *[resource.RESOURCE_RUBINS, 12001]
        )

        edit.downResource(resource.RESOURCE_RUBINS, 6000)
        edit.downResource(resource.RESOURCE_STEEL, 6000)
        edit.downResource(resource.RESOURCE_GOLD, 12.5)

        self.assertEqual(
            resource.getResources(),
            {
                resource.RESOURCE_RUBINS: 12000,
                resource.RESOURCE_WOOD: 0,
                resource.RESOURCE_STEEL: 12000,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 25
            }
        )

        Mapper.mapper.save(edit)

        self.assertEqual(
            resource.getResources(),
            {
                resource.RESOURCE_RUBINS: 6000,
                resource.RESOURCE_WOOD: 0,
                resource.RESOURCE_STEEL: 6000,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 12.5
            }
        )

    def testResource_Up_AfterGet(self):
        user = self.fixture.getUser(0)
        resource = user.getSubDomainResource()

        edit = resource.edit()
        edit.setResource(resource.RESOURCE_RUBINS, 12000)
        edit.setResource(resource.RESOURCE_STEEL, 12000)
        edit.setResource(resource.RESOURCE_GOLD, 25)
        Mapper.mapper.save(edit)

        edit = resource.edit()

        self.assertRaises(
            UserResourceExceptions.NotEnoughResource,
            edit.downResource,
            *[resource.RESOURCE_RUBINS, 12001]
        )

        edit.upResource(resource.RESOURCE_RUBINS, 6000)
        edit.upResource(resource.RESOURCE_STEEL, 6000)
        edit.upResource(resource.RESOURCE_GOLD, 12.5)

        self.assertEqual(
            resource.getResources(),
            {
                resource.RESOURCE_RUBINS: 12000,
                resource.RESOURCE_WOOD: 0,
                resource.RESOURCE_STEEL: 12000,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 25
            }
        )

        Mapper.mapper.save(edit)

        self.assertEqual(
            resource.getResources(),
            {
                resource.RESOURCE_RUBINS: 18000,
                resource.RESOURCE_WOOD: 0,
                resource.RESOURCE_STEEL: 18000,
                resource.RESOURCE_STONE: 0,
                resource.RESOURCE_EAT: 0,
                resource.RESOURCE_GOLD: 37.5
            }
        )
