from tests.backend.t_models.t_Resources import generic
from models.Resources import ResourcesDomain


class Backend_Models_Resources_ResourcesDomainTest(generic.Backend_Models_Resources_Generic):

    def testAddDomain(self):
        resourceDomain = ResourcesDomain.ResourcesDomain()
        resourceEdit = resourceDomain.edit()

        resourceEdit.setAmount(10000)
        resourceEdit.setBaseOutput(1000)
        resourceEdit.setOutput(1000)
        resourceEdit.setPosition(self.map)
        resourceEdit.setType(resourceDomain.TYPE_EAT)
        resourceEdit.setUser(self.user)
        resourceEdit.setTown(self.town)
        resourceEdit.getFactory().add(resourceEdit)

        self.assertEqual(resourceDomain.getUser(), self.user)
        self.assertEqual(resourceDomain.getTown(), self.town)
        self.assertEqual(resourceDomain.getPosition(), self.map)
        self.assertEqual(resourceDomain.getAmount(), 10000)
        self.assertEqual(resourceDomain.getOutput(), 1000)
        self.assertEqual(resourceDomain.getBaseOutput(), 1000)
        self.assertEqual(resourceDomain.getType(), resourceDomain.TYPE_EAT)

    def testEditDomain(self):
        resourceDomain = ResourcesDomain.ResourcesDomain()
        resourceEdit = resourceDomain.edit()
        resourceEdit.setAmount(10000)
        resourceEdit.setBaseOutput(1000)
        resourceEdit.setOutput(1000)
        resourceEdit.setPosition(self.map)
        resourceEdit.setType(resourceDomain.TYPE_EAT)
        resourceEdit.setUser(None)
        resourceEdit.setTown(None)
        resourceEdit.getFactory().add(resourceEdit)

        resourceEdit = resourceDomain.edit()
        resourceEdit.setUser(self.user)
        resourceEdit.setTown(self.town)
        resourceEdit.setOutput(100000)
        resourceEdit.setAmount(1000000)

        self.assertRaises(
            AssertionError,
            resourceEdit.setBaseOutput,
            10000
        )

        self.assertRaises(
            AssertionError,
            resourceEdit.setPosition,
            self.map
        )

        self.assertRaises(
            AssertionError,
            resourceEdit.setType,
            resourceDomain.TYPE_WOOD
        )

        self.assertRaises(
            AssertionError,
            resourceEdit.setPosition,
            self._fillMapOneItem(25, 25)
        )

        resourceEdit.getFactory().save(resourceEdit)

        self.assertEqual(resourceDomain.getUser(), self.user)
        self.assertEqual(resourceDomain.getTown(), self.town)
        self.assertEqual(resourceDomain.getOutput(), 100000)
        self.assertEqual(resourceDomain.getAmount(), 1000000)
