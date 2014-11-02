import service.TownBuilds
import service.Town


class AbstractResourceController(object):
    def _getParamsAclTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Acl', 'Params')


class MainController(AbstractResourceController):
    def createBuild(self, transfer, data):
        self._getParamsAclTownBuilds().create(
            transfer.getUser(),
            data['town'],
            data['key'],
            data['level']
        )

        transfer.send('/town_builds/create', {'done': True})

    def removeBuild(self, transfer, data):
        self._getParamsAclTownBuilds().remove(
            transfer.getUser(),
            data['town'],
            data['key'],
            data['level']
        )

        transfer.send('/town_builds/remove', {'done': True})
