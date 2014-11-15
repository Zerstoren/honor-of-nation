from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.TownController
import controller.TownBuildsController


class Backend_Controller_TownTest(Backend_Controller_Generic):
    def _getMainController(self):
        return controller.TownBuildsController.MainController()

    def _getModelController(self):
        return controller.TownController.ModelController()

    def testGetTownBuilds_Village(self):
        self.fillTerrain(0, 0, 3, 3)
        controller = self._getMainController()
        transfer = self._login()
        user = transfer.getUser()

        townDomain = self.addTown(0, 0, user, population=13000, typeTown=0, name='Systemd')

        controller.getTownBuilds(transfer, {
            'town': str(townDomain.getId())
        })

        self.assertDictEqual(
            transfer.getLastMessage(),
            {
                'async': None,
                'module': '/town_builds/get_builds',
                'message': {
                    'done': True,
                    'queue': [],
                    'builds': {
                        'v_council': 0,
                        'hut': 0,
                        'farm': 0,
                        'field': 0,
                        'mill': 0,
                        'mine': 0,
                        'road': 0
                    }
                },
            }
        )

    def testGetTownBuilds_City(self):
        self.fillTerrain(0, 0, 3, 3)
        controller = self._getMainController()
        transfer = self._login()
        user = transfer.getUser()

        townDomain = self.addTown(0, 0, user, population=13000, typeTown=1, name='Systemd')

        controller.getTownBuilds(transfer, {
            'town': str(townDomain.getId())
        })

        self.assertDictEqual(
            transfer.getLastMessage(),
            {
                'module': '/town_builds/get_builds',
                'async': None,
                'message':  {
                    'done': True,
                    'queue': [],
                    'builds':  {
                        'casern': 0,
                        't_council': 0,
                        'prison': 0,
                        'road': 0,
                        'farm': 0,
                        'field': 0,
                        'smithy': 0,
                        'wall': 0,
                        'mill': 0,
                        'storage': 0,
                        'mine': 0,
                        'guildhall': 0,
                        'house': 0
                    }
                }
            }
        )

    def testGetTownBuilds_Castle(self):
        self.fillTerrain(0, 0, 3, 3)
        controller = self._getMainController()
        transfer = self._login()
        user = transfer.getUser()

        townDomain = self.addTown(0, 0, user, population=13000, typeTown=2, name='Systemd')

        controller.getTownBuilds(transfer, {
            'town': str(townDomain.getId())
        })

        self.assertDictEqual(
            transfer.getLastMessage(),
            {
                'module': '/town_builds/get_builds',
                'async': None,
                'message': {
                    'done': True,
                    'queue': [],
                    'builds': {
                        'mine': 0,
                        'smithy': 0,
                        'high_wall': 0,
                        'barrack': 0,
                        'farm': 0,
                        'road': 0,
                        'headquarters': 0,
                        'casern': 0
                    }
                },
            }
        )

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
