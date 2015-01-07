from service.Resources import Service_Resources
from service.User import Service_User


class AbstractResourceController(object):
    def _getAclJsonPackResourceService(self):
        return Service_Resources().decorate(Service_Resources.ACL_JSONPACK)

    def _getJsonPackResourceService(self):
        return Service_Resources().decorate(Service_Resources.JSONPACK)

class ModelController(AbstractResourceController):
    def get(self, transfer, data):

        resourceService = self._getAclJsonPackResourceService()
        userDomain = Service_User().getUserDomain(data['user'])

        transfer.send('/model/resources/get', {
            'done': True,
            'result': resourceService.getResources(transfer.getUser(), userDomain)
        })


class DeliveryController(AbstractResourceController):
    def resourceChange(self, user):
        """
        :type user: models.User.Domain.User_Domain
        """
        user.getTransfer().forceSend('/delivery/resourceUpdate', {
            'done': True,
            'resources': self._getJsonPackResourceService().getResources(user)
        })
