from tests.backend.t_models.t_Towns import generic
from models.Towns import Factory, TownsDomain

import libs.mongo


class Backend_Models_Towns_TownsFactory(generic.Backend_Models_Towns_Generic):
    def _assertTownEqual(self, town, townDomain):
        self.assertIsInstance(town, TownsDomain.TownsDomain)
        self.assertIsInstance(townDomain, TownsDomain.TownsDomain)

        self.assertNotEqual(town, townDomain)

        self.assertEqual(
            townDomain.getId(),
            town.getId()
        )

        self.assertEqual(
            townDomain.getPosition(),
            town.getPosition()
        )

        self.assertEqual(
            townDomain.getUser(),
            town.getUser()
        )

        self.assertEqual(
            townDomain.getType(),
            town.getType()
        )


    def testCreateTown(self):
        domain = TownsDomain.TownsDomain()
        edit = domain.edit()

        self.user = self.fixture.getUser(0)

        edit\
            .setUser(self.user)\
            .setPosition(self.mapDomain)\
            .setType(domain.TYPE_CITY)\
            .setName('TestName')\
            .setPopulation(2500)

        Factory.factory.add(edit)

        content = libs.mongo.mongo['towns'].find_one({
            'user': self.user.getId(),
            'pos_id': self.mapDomain.getId()
        })

        self.assertEqual(len(content), 6)
        self.assertEqual(content['_id'], domain.getId())
        self.assertEqual(content['user'], self.user.getId())
        self.assertEqual(content['name'], 'TestName')
        self.assertEqual(content['pos_id'], self.mapDomain.getId())
        self.assertEqual(content['town_type'], domain.TYPE_CITY)
        self.assertEqual(content['population'], 2500)

    def testGetById(self):
        townDomain = self._createTown(self.mapDomain, self.user)
        Factory.factory._cleanIndexes()

        town = Factory.factory.getById(townDomain.getId())
        self._assertTownEqual(town, townDomain)

    def testGetByMap(self):
        townDomain = self._createTown(self.mapDomain, self.user)
        Factory.factory._cleanIndexes()

        town = Factory.factory.getByMap(self.mapDomain)
        self._assertTownEqual(town, townDomain)

    def testGetByUser(self):
        self.mapDomain1 = self._fillMapOneItem(42, 42)

        townDomain = self._createTown(self.mapDomain, self.user)
        townDomain1 = self._createTown(self.mapDomain1, self.user)

        Factory.factory._cleanIndexes()

        townsCollection = Factory.factory.getByUser(self.user)

        self._assertTownEqual(townsCollection[0], townDomain)
        self._assertTownEqual(townsCollection[1], townDomain1)

