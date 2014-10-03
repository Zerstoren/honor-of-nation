from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.UserController


class Backend_Controller_UserTest(Backend_Controller_Generic):
    def _getModelController(self):
        return controller.UserController.ModelController()

    def testLogin(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()

        controller.login(transfer, {
            'login': user.getLogin(),
            'password': user._domain_data['_testPassword']
        })

        message = transfer.getLastMessage()

        self.assertDictEqual(message, {
            'module': '/model/user/login',
            'async': None,
            'message': {
                'auth_result': True,
                'done': True,
                'data': {
                    'user': {
                        'login': user.getLogin(),
                        '_id': str(user.getId()),
                        'admin': True,
                        'position': {'x': 1, 'y': 1},
                        '_testPassword': '12345'
                    },
                    'resources': {
                        'rubins': 1000000,
                        'steel': 1000000,
                        'eat': 1000000,
                        'wood': 1000000,
                        'stone': 1000000,
                        'gold': 1000000
                    }
                }
            }
        })

    def testLogin_WrongLoginOrPassword(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()

        controller.login(transfer, {
            'login': 'asdasdsadasdas',
            'password': 'dfsdfsdfsfsdfsdf'
        })

        message = transfer.getLastMessage()

        self.assertDictEqual(message, {
            'module': '/model/user/login',
            'async': None,
            'message': {
                'auth_result': False,
                'done': True,
                'data': None
            }
        })

        controller.login(transfer, {
            'login': user.getLogin(),
            'password': 'dfsdfsdfsfsdfsdf'
        })

        message = transfer.getLastMessage()

        self.assertDictEqual(message, {
            'module': '/model/user/login',
            'async': None,
            'message': {
                'auth_result': False,
                'done': True,
                'data': None
            }
        })
