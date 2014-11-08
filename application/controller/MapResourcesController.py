import service.MapResources
import helpers.MapCoordinate


class AbstractResourceController(object):
    def _getParamsAclJsonPackMapResources(self):
        return service.MapResources.Service_MapResources().decorate('Acl', 'JsonPack')

class ModelController(AbstractResourceController):
    def get(self, transfer, data):
        result = {}
        result['done'] = True
        result['data'] = self._getParamsAclJsonPackMapResources().getResourceByPosition(
            helpers.MapCoordinate.MapCoordinate(posId=data['posId']),
            transfer.getUser()
        )

        transfer.send('/model/map_resources/get', result)
