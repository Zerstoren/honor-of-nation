from tests.backend.t_models.t_Map import generic
from models.Map import Factory
from models.Map import Exceptions


class Backend_Model_Map_MapFactoryTest(generic.Backend_Models_Map_Generic):

    def testMapAdd(self):
        mapDomain, mapEdit = Factory.factory.createMap()

        mapEdit.setPosition(10, 10)
        mapEdit.setLand(mapDomain.LAND_VALLEY)
        mapEdit.setDecor(0)
        mapEdit.setBuild(mapDomain.BUILD_EMPTY)
        mapEdit.setBuildType(0)

        mapEdit.getFactory().add(mapEdit)

        domain = Factory.factory.getByPosition(10, 10)

        self.assertEquals(mapDomain, domain)

    def testMapSave(self):
        domain = self._createMapCell(40, 40)

        writed = domain.edit()

        writed.setLand(domain.LAND_JUNGLE)
        writed.setLandType(3)
        Factory.factory.save(writed)

        self.assertEqual(domain.getPositionX(), 40)
        self.assertEqual(domain.getPositionY(), 40)
        self.assertEqual(domain.getLand(), domain.LAND_JUNGLE)
        self.assertEqual(domain.getLandType(), 3)

    def testMapGetById_Position(self):
        createDomain = self._createMapCell(0, 0)
        factoryDomainId = Factory.factory.getById(0)
        factoryDomainPosition = Factory.factory.getByPosition(0, 0)

        self.assertEqual(createDomain, factoryDomainId)
        self.assertEqual(createDomain, factoryDomainPosition)

    def testMapGetChunk(self):
        for x in range(17):
            for y in range(16):
                self._createMapCell(x, y)

        domain = Factory.factory.getByPosition(0, 0)

        collection = Factory.factory.getByChunk(domain.getChunk())
        self.assertEqual(len(collection), 256)

    def testMapGetChunk_ForUser(self):
        user = self.fixture.getUser(0)

        for x in range(5):
            for y in range(5):
                self._createMapCell(x, y)

        domain = Factory.factory.getByPosition(0, 0)

        collection = Factory.factory.getByChunk(domain.getChunk())
        self.assertFalse(collection.isVisibleFor(user))
        collection.addAccessToUser(user)
        self.assertTrue(collection.isVisibleFor(user))

    def testMapGetById_ForUser(self):
        user = self.fixture.getUser(0)
        domain = self._createMapCell(0, 0)

        self.assertRaises(
            Exceptions.UserNotSeeTheCell,
            Factory.factory.getByIdUser,
            *[0, user]
        )

        domain.addAccessToUser(user)

        domainFactoryUser = Factory.factory.getByIdUser(0, user)

        self.assertEqual(
            domain,
            domainFactoryUser
        )

    def testMapGetByPosition_ForUser(self):
        user = self.fixture.getUser(0)
        domain = self._createMapCell(0, 0)

        self.assertRaises(
            Exceptions.UserNotSeeTheCell,
            Factory.factory.getByPositionUser,
            *[0, 0, user]
        )

        domain.addAccessToUser(user)

        domainFactoryUser = Factory.factory.getByPositionUser(0, 0, user)

        self.assertEqual(
            domain,
            domainFactoryUser
        )
