from service.Town import Service_Town
from service.User import Service_User
from service.TownBuilds import Service_TownBuilds
import helpers.MapCoordinate


class AbstractTownController(object):
    def _getAclParamsJsonPackTown(self):
        return Service_Town().decorate(Service_Town.PARAMS_JSONPACK_ACL)

    def _getParamsAclJsonPackTown(self):
        return Service_Town().decorate(Service_Town.JSONPACK_ACL)

    def _getParamsAclJsonPackUser(self):
        return Service_User().decorate(Service_User.JSONPACK)

    def _getParamsAclJsonPackTownBuilds(self):
        return Service_TownBuilds().decorate(Service_TownBuilds.PARAMS_JSONPACK_ACL)


class ModelController(AbstractTownController):
    def get(self, transfer, data):
        result = {}
        result['done'] = True
        result['data'] = self._getParamsAclJsonPackTown().getById(data['id'])
        result['data']['user'] = self._getParamsAclJsonPackUser().getUserDomain(result['data']['user'])

        transfer.send('/model/town/get_pos_id', result)


    def get_pos_id(self, transfer, data):
        position = helpers.MapCoordinate.MapCoordinate(posId=data['posId'])

        result = {}
        result['done'] = True
        result['data'] = self._getParamsAclJsonPackTown().loadByPosition(position)
        result['data']['user'] = self._getParamsAclJsonPackUser().getUserDomain(result['data']['user'])

        transfer.send('/model/town/get_pos_id', result)
