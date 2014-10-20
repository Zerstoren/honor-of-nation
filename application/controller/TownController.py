import service.Town
import service.User
import helpers.MapCoordinate


class AbstractResourceController(object):
    def _getParamsAclJsonPackTown(self):
        return service.Town.Service_Town().decorate('Acl', 'JsonPack')

    def _getParamsAclJsonPackUser(self):
        return service.User.Service_User().decorate('JsonPack')

class ModelController(AbstractResourceController):
    def get(self, transfer, data):
        position = helpers.MapCoordinate.MapCoordinate(posId=data['posId'])

        result = {}
        result['done'] = True
        result['data'] = self._getParamsAclJsonPackTown().loadByPosition(position)
        result['data']['user'] = self._getParamsAclJsonPackUser().getUserDomain(result['data']['user'])

        transfer.send('/model/town/get', result)
