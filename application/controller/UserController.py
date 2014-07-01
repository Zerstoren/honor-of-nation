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
        userService = self._getAclPackUserService()

        result, domainDict = userService.login(data['login'], data['password'])

        if domainDict is not None:
            userDomain = userService.getUserDomain(domainDict['_id'])
            userDomain._setTransfer(transfer)
            transfer.setUser(userDomain)

        transfer.send('/model/user/login', {
            'done': True,
            'auth_result': result,
            'data': domainDict
        })


class CollectionController(_AbstractUserController):
    pass
