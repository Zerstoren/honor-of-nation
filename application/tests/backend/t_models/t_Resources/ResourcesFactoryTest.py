from tests.backend.t_models.t_Resources import generic
from models.Resources import Factory


class Backend_Models_Resources_ResourcesFactoryTest(generic.Backend_Models_Resources_Generic):
    def testGetById(self):
        resource = self._createResource(
            self.map,
            user=self.user,
            town=self.town
        )

        self.fullCleanCache()

        res = Factory.factory.getById(resource.getId())
        self.assertEqual(len(res._getData().keys()), 8)
        self.assertEqual(res._getData(), resource._getData())

        # From cache
        res = Factory.factory.getById(resource.getId())
        self.assertEqual(len(res._getData().keys()), 8)
        self.assertEqual(res._getData(), resource._getData())

    def testGetByMap(self):
        resource = self._createResource(
            self.map,
            user=self.user,
            town=self.town
        )

        self.fullCleanCache()

        res = Factory.factory.getByMap(self.map)
        self.assertEqual(len(res._getData().keys()), 8)
        self.assertEqual(res._getData(), resource._getData())

        # From cache
        res = Factory.factory.getByMap(self.map)
        self.assertEqual(len(res._getData().keys()), 8)
        self.assertEqual(res._getData(), resource._getData())

    def testGetByUser(self):
        map1 = self._fillMapOneItem(35, 35)
        map2 = self._fillMapOneItem(35, 36)
        map3 = self._fillMapOneItem(35, 37)

        user = self.fixture.getUser(1)

        res1 = self._createResource(map1, self.user, None)
        res2 = self._createResource(map2, self.user, None)
        res3 = self._createResource(map3, user, None)

        self.fullCleanCache()

        collection = Factory.factory.getByUser(self.user)
        self.assertEqual(len(collection[0]._getData().keys()), 8)
        self.assertEqual(collection[0]._getData(), res1._getData())
        self.assertEqual(len(collection[1]._getData().keys()), 8)
        self.assertEqual(collection[1]._getData(), res2._getData())

        collection2 = Factory.factory.getByUser(user)
        self.assertEqual(len(collection2[0]._getData().keys()), 8)
        self.assertEqual(collection2[0]._getData(), res3._getData())

        # From cache
        collection = Factory.factory.getByUser(self.user)
        self.assertEqual(len(collection[0]._getData().keys()), 8)
        self.assertEqual(collection[0]._getData(), res1._getData())
        self.assertEqual(len(collection[1]._getData().keys()), 8)
        self.assertEqual(collection[1]._getData(), res2._getData())

        collection2 = Factory.factory.getByUser(user)
        self.assertEqual(len(collection2[0]._getData().keys()), 8)
        self.assertEqual(collection2[0]._getData(), res3._getData())

    def testGetByTown(self):
        map1 = self._fillMapOneItem(34, 35)
        map2 = self._fillMapOneItem(34, 36)
        map3 = self._fillMapOneItem(34, 37)

        map11 = self._fillMapOneItem(35, 35)
        map22 = self._fillMapOneItem(35, 36)

        user = self.fixture.getUser(1)

        town = self._createTown(map11, self.user)
        town1 = self._createTown(map22, user)

        res1 = self._createResource(map1, self.user, town)
        res2 = self._createResource(map2, self.user, town)
        res3 = self._createResource(map3, user, town1)

        self.fullCleanCache()

        collection = Factory.factory.getByTown(town)
        self.assertEqual(len(collection[0]._getData().keys()), 8)
        self.assertEqual(collection[0]._getData(), res1._getData())

        self.assertEqual(len(collection[1]._getData().keys()), 8)
        self.assertEqual(collection[1]._getData(), res2._getData())

        collection2 = Factory.factory.getByTown(town1)
        self.assertEqual(len(collection2[0]._getData().keys()), 8)
        self.assertEqual(collection2[0]._getData(), res3._getData())

        # From cache
        collection = Factory.factory.getByTown(town)
        self.assertEqual(len(collection[0]._getData().keys()), 8)
        self.assertEqual(collection[0]._getData(), res1._getData())
        self.assertEqual(len(collection[1]._getData().keys()), 8)
        self.assertEqual(collection[1]._getData(), res2._getData())

        collection2 = Factory.factory.getByTown(town1)
        self.assertEqual(len(collection2[0]._getData().keys()), 8)
        self.assertEqual(collection2[0]._getData(), res3._getData())

