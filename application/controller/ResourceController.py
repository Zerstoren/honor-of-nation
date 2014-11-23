import service.Resources
import service.User


class AbstractResourceController(object):
    def _getAclJsonPackResourceService(self):
        return service.Resources.Service_Resources().decorate('Acl', 'JsonPack')

    def _getJsonPackResourceService(self):
        return service.Resources.Service_Resources().decorate('JsonPack')

class ModelController(AbstractResourceController):
    def get(self, transfer, data):

        resourceService = self._getAclJsonPackResourceService()
        userDomain = service.User.Service_User().getUserDomain(data['user'])

        transfer.send('/model/resources/get', {
            'done': True,
            'result': resourceService.getResources(transfer.getUser(), userDomain)
        })


class DeliveryController(AbstractResourceController):
    def resourceChange(self, user):
        """
        :type user: models.User.Domain.User_Domain
        """
        user.getTransfer().send('/delivery/resourceUpdate', {
            'done': True,
            'resources': self._getJsonPackResourceService().getResources(user)
        })
