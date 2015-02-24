from service.MapResources import Service_MapResources
from service.Town import Service_Town
import helpers.MapCoordinate


class AbstractResourceController(object):
    def _getParamsAclJsonPackMapResources(self):
        return Service_MapResources().decorate(Service_MapResources.JSONPACK_ACL)

class ModelController(AbstractResourceController):
    def get(self, transfer, data):
        result = {}
        result['done'] = True
        result['data'] = self._getParamsAclJsonPackMapResources().getResourceByPosition(
            helpers.MapCoordinate.MapCoordinate(posId=data['posId']),
            transfer.getUser()
        )

        transfer.send('/model/map_resources/get', result)


class DeliveryController(AbstractResourceController):
    def resourcesUpdate(self, town, resources):
        town.getUser().getTransfer().forceSend('/delivery/mapResourcesUpdate', {
            'done': True,
            'resources': resources
        })


class CeleryPrivateController(AbstractResourceController):
    def resourceDown(self):
        serviceTown = Service_Town()
        serviceMapResources = Service_MapResources()
        serviceMapResourcesJsonPack = Service_MapResources().getDecorateClass(Service_MapResources.JSONPACK)
        deliveryController = DeliveryController()

        townCollection = serviceTown.getAllTownsCollection()
        for town in townCollection:
            resources = serviceMapResources.getResourceByTown(town)
            townBonus = town.getBonus()
            sendResources = []

            for resource in resources:
                serviceMapResources.resourceDown(resource)
                sendResources.append(
                    serviceMapResourcesJsonPack.packDomainToJson(resource)
                )

            deliveryController.resourcesUpdate(town, sendResources)


