import service.Town
import service.User
import service.TownBuilds
import helpers.MapCoordinate


class AbstractTownController(object):
    def _getParamsTown(self):
        return service.Town.Service_Town().decorate('Params')

    def _getAclParamsJsonPackTown(self):
        return service.Town.Service_Town().decorate('Acl', 'Params', 'JsonPack')

    def _getParamsAclJsonPackTown(self):
        return service.Town.Service_Town().decorate('Acl', 'JsonPack')

    def _getParamsAclJsonPackUser(self):
        return service.User.Service_User().decorate('JsonPack')

    def _getParamsAclJsonPackTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Params', 'Acl', 'JsonPack')

    def _getAclJsonPackTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Acl', 'JsonPack')


class MainController(AbstractTownController):
    def getTownBuilds(self, transfer, data):
        townDomain = self._getParamsTown().getById(data['id'])

        result = {}
        result['done'] = True
        result['data'] = self._getAclJsonPackTownBuilds().get(
            townDomain,
            transfer.getUser()
        )

        transfer.send('/town/get_builds', result)


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
