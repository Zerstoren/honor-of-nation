from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.AdminController
import exceptions.httpCodes
import exceptions.database


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
            "fillLand": "valley",
            "fillLandType": 1,
            "type": "coordinate",
        })

        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])

    def testFillTerrainChunks(self):
        controller = self._getModelController()
        transfer = self._login()
        self.setUserAsAdmin(transfer.getUser())

        controller.fillTerrain(transfer, {
            "chunks": [1],
            "fillLand": "valley",
            "fillLandType": 1,
            "type": "chunks",
        })

        message = transfer.getLastMessage()['message']
        self.assertTrue(message['done'])

    def testFillTerrain_ExpectedException(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()
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
                "fillLand": "valley",
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
            'login': 'Zerst',
            'admin': True
        })
        self.assertEqual(message['resources'], {
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

        controller.searchUser(transfer, {
            'login': 'notFoundUser'
        })

        message = transfer.getLastMessage()['message']
        self.assertFalse(message['done'])
        self.assertEqual(message['error'], 'User with login notFoundUser not found')


    def testSearchUser_AdminCantEditAdmin(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()
        user2 = self.fixture.getUser(2)

        self.setUserAsAdmin(user)
        self.setUserAsAdmin(user2)

        controller.searchUser(transfer, {
            'login': user2.getLogin()
        })

        message = transfer.getLastMessage()['message']
        self.assertFalse(message['done'])
        self.assertEqual(message['error'], 'Can`t edit other admin')

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
