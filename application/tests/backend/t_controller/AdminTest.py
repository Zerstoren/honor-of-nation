from system.mongo import exceptions
from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.AdminController

import service.MapResources

import exceptions.httpCodes
import exceptions.database
import exceptions.args

import models.MapUserVisible.Mapper
import models.Map.Mapper

import models.Map.Factory

import helpers.MapCoordinate


class Backend_Controller_AdminTest(Backend_Controller_Generic):
    def _getModelController(self):
        return controller.AdminController.MainAdminController()

    def testFillTerrain(self):
        controller = self._getModelController()
        transfer = self._login()
        self.setUserAsAdmin(transfer.getUser())

        controller.fillTerrain(transfer, {
            "coordinate": {
                "fromX": 1,
                "fromY": 1,
                "toX": 4,
                "toY": 4
            },
            "fillLand": "1",
            "fillLandType": 1,
            "type": "coordinate",
        })

        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])

    def testFillTerrain_WrongType(self):
        controller = self._getModelController()
        transfer = self._login()
        self.setUserAsAdmin(transfer.getUser())

        self.assertRaises(
            ValueError,
            controller.fillTerrain,
            transfer,
            {
                "coordinate": {
                    "fromX": 1,
                    "fromY": 1,
                    "toX": 1,
                    "toY": 1
                },
                "fillLand": "valley",
                "fillLandType": 1,
                "type": "coordinate",
            }
        )

        self.assertRaises(
            ValueError,
            controller.fillTerrain,
            transfer,
            {
                "coordinate": {
                    "fromX": 1,
                    "fromY": 1,
                    "toX": 1,
                    "toY": 1
                },
                "fillLand": "1",
                "fillLandType": "wat?",
                "type": "coordinate",
            }
        )

    def testFillTerrain_WrongFillType(self):
        controller = self._getModelController()
        transfer = self._login()
        self.setUserAsAdmin(transfer.getUser())

        controller.fillTerrain(transfer, {
            "coordinate": {
                "fromX": 1,
                "fromY": 1,
                "toX": 4,
                "toY": 4
            },
            "fillLand": "1",
            "fillLandType": 1,
            "type": "asdasd",
        })

        message = transfer.getLastMessage()['message']
        self.assertFalse(message['done'])
        self.assertEqual(message['error'], 'Переданы неверные параметры заполнения территории')

    def testFillTerrainChunks(self):
        controller = self._getModelController()
        transfer = self._login()
        self.setUserAsAdmin(transfer.getUser())

        controller.fillTerrain(transfer, {
            "chunks": [1],
            "fillLand": "1",
            "fillLandType": 1,
            "type": "chunks",
        })

        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])

    def testFillTerrain_ExpectedException(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()
        user.setAdmin(False)
        user.getMapper().save(user)

        self.assertRaises(
            exceptions.httpCodes.Page403,
            controller.fillTerrain,
            transfer,
            {
                "coordinate": {
                    "fromX": 1,
                    "fromY": 1,
                    "toX": 1,
                    "toY": 1
                },
                "fillLand": "1",
                "fillLandType": 1,
                "type": "coordinate",
            }
        )

    def testFillTerrain_WrongCoordinates(self):
        controller = self._getModelController()
        transfer = self._login()
        self.setUserAsAdmin(transfer.getUser())

        coords = [
            (-1, 0, 0, 0),
            (0, -1, 0, 0),
            (0, 0, -1, 0),
            (0, 0, 0, -1),
            (10, 0, 9, 0),
            (0, 10, 0, 9),
        ]

        for coord in coords:
            self.assertRaises(
                exceptions.args.Arguments,
                controller.fillTerrain,
                transfer,
                {
                    "coordinate": {
                        "fromX": coord[0],
                        "fromY": coord[1],
                        "toX": coord[2],
                        "toY": coord[3]
                    },
                    "fillLand": "1",
                    "fillLandType": 1,
                    "type": "coordinate",
                }
            )

    def testSearchUser(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()

        self.setUserAsAdmin(user)

        controller.searchUser(transfer, {
            'login': user.getLogin()
        })

        data = transfer.getLastMessage()
        message = data['message']

        self.assertEqual(data['module'], '/admin/searchUser')
        self.assertEqual(message['done'], True)
        self.assertEqual(message['user'], {
            '_id' : str(user.getId()),
            'login': 'Zerst',
            'admin': True
        })
        self.assertEqual(message['resources'], {
            '_id': str(user.getResources().getId()),
            'user': str(user.getId()),
            'eat': 1000000,
            'gold': 1000000,
            'rubins': 1000000,
            'stone': 1000000,
            'wood': 1000000,
            'steel': 1000000
        })

    def testSearchUser_UserNotFound(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()

        self.setUserAsAdmin(user)

        self.assertRaises(
            exceptions.message.Message,
            controller.searchUser,
            transfer,
            {
                'login': 'notFoundUser'
            }
        )


    def testSearchUser_AdminCantEditAdmin(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()
        user2 = self.fixture.getUser(2)

        self.setUserAsAdmin(user)
        self.setUserAsAdmin(user2)

        self.assertRaises(
            exceptions.httpCodes.Page403,
            controller.searchUser,
            transfer,
            {
                'login': user2.getLogin()
            }
        )

    def testSaveResources(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()
        self.setUserAsAdmin(user)

        controller.saveResources(transfer, {
            'userLogin': user.getLogin(),
            'resources': {
                'rubins': 10,
                'wood': 100,
                'steel': 500,
                'stone': 1000,
                'eat': 5000,
                'gold': 10000
            }
        })

        resources = user.getResources()

        # Message delivery
        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])
        self.assertEqual(resources.getRubins(), message['resources']['rubins'])
        self.assertEqual(resources.getWood(), message['resources']['wood'])
        self.assertEqual(resources.getSteel(), message['resources']['steel'])
        self.assertEqual(resources.getStone(), message['resources']['stone'])
        self.assertEqual(resources.getEat(), message['resources']['eat'])
        self.assertEqual(resources.getGold(), message['resources']['gold'])

        # Controller send
        message = transfer.getLastMessage(1)['message']
        self.assertTrue(message['done'])
        self.assertEqual(resources.getRubins(), 10)
        self.assertEqual(resources.getWood(), 100)
        self.assertEqual(resources.getSteel(), 500)
        self.assertEqual(resources.getStone(), 1000)
        self.assertEqual(resources.getEat(), 5000)
        self.assertEqual(resources.getGold(), 10000)

    def testSaveCoordinate(self):
        self.fillTerrain(0, 0, 3, 3)

        controller = self._getModelController()
        transfer = self._login()
        self.setUserAsAdmin(transfer.getUser())
        controller.saveCoordinate(transfer, {
            'fromX': 0,
            'fromY': 0,
            'toX': 2,
            'toY': 2
        })

        self.assertTrue(
            transfer.getLastMessage()['message']['done']
        )

        self.assertEqual(
            9,
            models.MapUserVisible.Mapper.MapUserVisible_Mapper._select().count()
        )

        self.assertEqual(
            16,
            models.Map.Mapper.Map_Mapper._select().count()
        )

    def testLoadResourceMap_NoResources(self):
        self.fillTerrain(0, 0, 3, 3)
        self.addResource(0, 0, 'rubins')

        controller = self._getModelController()
        transfer = self._login()

        controller.loadResourceMap(transfer, {
            'x': False,
            'y': False
        })

        result = transfer.getLastMessage()['message']
        self.assertTrue(result['done'])
        self.assertFalse(result['resource'])
        self.assertEqual(type(result['users']), list)
        self.assertEqual(result['users'][0]['login'], 'Zerst')

    def testLoadResourceMap_HasResources(self):
        self.fillTerrain(0, 0, 3, 3)
        self.addResource(0, 0, 'rubins')

        controller = self._getModelController()
        transfer = self._login()

        controller.loadResourceMap(transfer, {
            'x': 0,
            'y': 0
        })

        result = transfer.getLastMessage()['message']
        self.assertTrue(result['done'])
        self.assertEqual(result['resource']['pos_id'], 0)
        self.assertEqual(type(result['users']), list)
        self.assertEqual(result['users'][0]['login'], 'Zerst')

    def testLoadResourceMap_ResourcesNotFound(self):
        self.fillTerrain(0, 0, 3, 3)

        controller = self._getModelController()
        transfer = self._login()

        controller.loadResourceMap(transfer, {
            'x': 0,
            'y': 0
        })

        result = transfer.getLastMessage()['message']
        self.assertTrue(result['done'])
        self.assertFalse(result['resource'])
        self.assertEqual(type(result['users']), list)
        self.assertEqual(result['users'][0]['login'], 'Zerst')

        #
    def testSaveMapResource(self):
        self.fillTerrain(0, 0, 3, 3)

        controller = self._getModelController()
        transfer = self._login()

        self.setUserAsAdmin(transfer.getUser())

        controller.saveResourceDomain(transfer, {
            "domain": {
                "amount": 2500000,
                "base_output": 13000,
                "output": 0,
                "position": '1x1',
                "town": None,
                "type": "rubins",
                "user": str(transfer.getUser().getId())
            }
        })

        result = transfer.getLastMessage()['message']
        mapDomain = models.Map.Factory.Map_Factory.getDomainByPosition(1,1)
        mapResourceDomain = mapDomain.getResource()

        self.assertTrue(result['done'])
        self.assertEqual(mapDomain.getPosId(), mapResourceDomain.getPosId())
        self.assertEqual(2500000, mapResourceDomain.getAmount())
        self.assertEqual(13000, mapResourceDomain.getBaseOutput())
        self.assertEqual('rubins', mapResourceDomain.getType())
        self.assertEqual(str(mapResourceDomain.getUser().getId()), str(transfer.getUser().getId()))

    def testSaveMapResource_WithNoneUser(self):
        self.fillTerrain(0, 0, 3, 3)

        controller = self._getModelController()
        transfer = self._login()

        self.setUserAsAdmin(transfer.getUser())

        controller.saveResourceDomain(transfer, {
            "domain": {
                "amount": 2500000,
                "base_output": 13000,
                "output": 0,
                "position": '1x1',
                "town": None,
                "type": "rubins",
                "user": 'none'
            }
        })

        result = transfer.getLastMessage()['message']
        mapDomain = models.Map.Factory.Map_Factory.getDomainByPosition(1,1)
        mapResourceDomain = mapDomain.getResource()

        self.assertTrue(result['done'])
        self.assertEqual(mapResourceDomain.getUser(), None)

    def testUpdateMapResource(self):
        service.MapResources.Service_MapResources().saveResources({
            'amount': 500000,
            'base_output': 5000,
            'output': 5000,
            'posId': 2001,
            'town': None,
            'user': None,
            'type': 'steel'
        })

        resourceDomain = service.MapResources.Service_MapResources().getResourceByPosition(
            helpers.MapCoordinate.MapCoordinate(x=1, y=1)
        )

        self.fillTerrain(0, 0, 3, 3)

        controller = self._getModelController()
        transfer = self._login()

        self.setUserAsAdmin(transfer.getUser())

        controller.saveResourceDomain(transfer, {
            "domain": {
                "_id": str(resourceDomain.getId()),
                "amount": 2500000,
                "base_output": 13000,
                "output": 0,
                "position": '1x1',
                "town": None,
                "type": "rubins",
                "user": 'none'
            }
        })

        result = transfer.getLastMessage()['message']
        mapDomain = models.Map.Factory.Map_Factory.getDomainByPosition(1,1)
        mapResourceDomain = mapDomain.getResource()

        self.assertTrue(result['done'])
        self.assertEqual(mapResourceDomain.getUser(), None)
        self.assertEqual(mapResourceDomain.getgetAmount(), 2500000)
        self.assertEqual(mapResourceDomain.getType(), "rubins")
