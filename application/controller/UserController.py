import service.User

class _AbstractUserController(object):
    def _getAclUserService(self):
        return service.User.Service_User().decorate('Acl')

    def _getAclPackUserService(self):
        return service.User.Service_User().decorate('Acl', 'JsonPack')


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
                    'resources': domain.getResources().toDict()
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
