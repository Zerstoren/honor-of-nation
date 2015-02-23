from service.Resources import Service_Resources
from service.User import Service_User

import config


class AbstractResourceController(object):
    def _getResourcesService(self):
        return Service_Resources()

    def _getAclJsonPackResourceService(self):
        return Service_Resources().decorate(Service_Resources.JSONPACK_ACL)

    def _getJsonPackResourceService(self):
        return Service_Resources().decorate(Service_Resources.JSONPACK)

    def _getUserService(self):
        return Service_User()

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


class CeleryPrivateController(AbstractResourceController):
    def calculateResources(self):
        deliveryController = DeliveryController()
        serviceResources = self._getResourcesService()
        part = int(config.get('resource_updates.base')) / int(config.get('resource_updates.celery'))

        for user in self._getUserService().getAllUsers():
            serviceResources.updateResource(user, part)
            deliveryController.resourceChange(user)
