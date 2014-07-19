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
