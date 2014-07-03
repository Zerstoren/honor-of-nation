from tests.backend.t_controller.generic import Backend_Controller_Generic

import controller.MapController


class Backend_Controller_UserTest(Backend_Controller_Generic):
    def _getModelController(self):
        return controller.MapController.MainController()

    def testGettingUsersChunks(self):
        controller = self._getModelController()
        transfer = self._login()
        user = transfer.getUser()

        self._fillMap()

        controller.load_chunks(transfer, {
            'chunkList': [1, 2, 3]
        })

        message = transfer.getLastMessage()
        print(message)

    # def testLogin(self):
    #     controller = self._getModelController()
    #     transfer = self._login()
    #     user = transfer.getUser()
    #
    #     controller.login(transfer, {
    #         'login': user.getLogin(),
    #         'password': user._testPassword
    #     })
    #
    #     message = transfer.getLastMessage()
    #
    #     self.assertDictEqual(message, {
    #         'module': '/model/user/login',
    #         'async': None,
    #         'message': {
    #             'auth_result': True,
    #             'done': True,
    #             'data': {
    #                 'login': user.getLogin(),
    #                 '_id': str(user.getId())
    #             }
    #         }
    #     })
    #
    # def testLogin_WrongLoginOrPassword(self):
    #     controller = self._getModelController()
    #     transfer = self._login()
    #     user = transfer.getUser()
    #
    #     controller.login(transfer, {
    #         'login': 'asdasdsadasdas',
    #         'password': 'dfsdfsdfsfsdfsdf'
    #     })
    #
    #     message = transfer.getLastMessage()
    #
    #     self.assertDictEqual(message, {
    #         'module': '/model/user/login',
    #         'async': None,
    #         'message': {
    #             'auth_result': False,
    #             'done': True,
    #             'data': None
    #         }
    #     })
    #
    #     controller.login(transfer, {
    #         'login': user.getLogin(),
    #         'password': 'dfsdfsdfsfsdfsdf'
    #     })
    #
    #     message = transfer.getLastMessage()
    #
    #     self.assertDictEqual(message, {
    #         'module': '/model/user/login',
    #         'async': None,
    #         'message': {
    #             'auth_result': False,
    #             'done': True,
    #             'data': None
    #         }
    #     })
