from service.User import Service_User

class _AbstractUserController(object):
    def _getAclUserService(self):
        return Service_User().decorate(Service_User.ACL)

    def _getParamsUserService(self):
        return Service_User().decorate(Service_User.PARAMS)

    def _getJsonPackUserService(self):
        return Service_User().decorate(Service_User.JSONPACK)

    def _getAclPackUserService(self):
        return Service_User().decorate(Service_User.JSONPACK_ACL)


class MainController(_AbstractUserController):
    pass


class ModelController(_AbstractUserController):

    def login(self, transfer, data):
        userService = self._getAclUserService()

        domain = userService.login(data['login'], data['password'])

        if domain is not False:
            transfer.setUser(domain)
            transfer.send('/model/user/login', {
                'done': True,
                'auth_result': True,
                'data': {
                    'user': domain.toDict(),
                    'resources': domain.getResources().toDict(),
                    'states': self._getJsonPackUserService().getUserStates(domain)
                }
            })
        else:
            transfer.send('/model/user/login', {
                'done': True,
                'auth_result': False,
                'data': None
            })


class CollectionController(_AbstractUserController):
    pass
