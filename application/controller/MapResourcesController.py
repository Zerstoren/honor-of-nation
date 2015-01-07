from service.MapResources import Service_MapResources
import helpers.MapCoordinate


class AbstractResourceController(object):
    def _getParamsAclJsonPackMapResources(self):
        return Service_MapResources().decorate(Service_MapResources.ACL_JSONPACK)

class ModelController(AbstractResourceController):
    def get(self, transfer, data):
        result = {}
        result['done'] = True
        result['data'] = self._getParamsAclJsonPackMapResources().getResourceByPosition(
            helpers.MapCoordinate.MapCoordinate(posId=data['posId']),
            transfer.getUser()
        )

        transfer.send('/model/map_resources/get', result)
