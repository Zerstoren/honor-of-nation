import service.Resources
import service.User


class AbstractResourceController(object):
    def _getAclJsonPackResourceService(self):
        return service.Resources.Service_Resources().decorate('Acl', 'JsonPack')


class ModelController(AbstractResourceController):
    def get(self, transfer, data):

        resourceService = self._getAclJsonPackResourceService()
        userDomain = service.User.Service_User().getUserDomain(data['user'])

        transfer.send('/model/resources/get', {
            'done': True,
            'result': resourceService.getResources(transfer.getUser(), userDomain)
        })
