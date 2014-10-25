from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.TownController


class Backend_Controller_UserTest(Backend_Controller_Generic):
    def _getModelController(self):
        return controller.TownController.ModelController()

    def testTownModelGetByPosId(self):
        self.fillTerrain(0, 0, 3, 3)
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()

        townDomain = self.addTown(0, 0, user, population=13000, typeTown=1, name='Systemd')

        controller.get_pos_id(transfer, {
            'posId': 0
        })

        self.assertEqual(transfer.getLastMessage(), {
            'message': {
                'done': True,
                'data': {
                    '_id' : str(townDomain.getId()),
                    "type": 1,
                    "user": str(user.getId()),
                    "population": 13000,
                    "pos_id": 0,
                    "name": 'Systemd',
                    'user': {
                        '_id': str(user.getId()),
                        'login': user.getLogin(),
                        'position': user.getPosition()
                    }
                }
            },
            'async': None,
            'module': '/model/town/get_pos_id'
        })

    def testTownModelGetById(self):
        self.fillTerrain(0, 0, 3, 3)
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()

        townDomain = self.addTown(0, 0, user, population=13000, typeTown=1, name='Systemd')

        controller.get(transfer, {
            'id': str(townDomain.getId())
        })

        self.assertEqual(transfer.getLastMessage(), {
            'message': {
                'done': True,
                'data': {
                    '_id' : str(townDomain.getId()),
                    "type": 1,
                    "user": str(user.getId()),
                    "population": 13000,
                    "pos_id": 0,
                    "name": 'Systemd',
                    'user': {
                        '_id': str(user.getId()),
                        'login': user.getLogin(),
                        'position': user.getPosition()
                    }
                }
            },
            'async': None,
            'module': '/model/town/get_pos_id'
        })
