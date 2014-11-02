import service.TownBuilds
import service.Town


class AbstractResourceController(object):
    def _getParamsTown(self):
        return service.Town.Service_Town().decorate('Params')

    def _getAclJsonPackTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Acl', 'JsonPack')

    def _getParamsAclTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Acl', 'Params')


class MainController(AbstractResourceController):
    def _getBuildsAndQueueData(self, transfer, townDomain):
        townBuildsService = self._getAclJsonPackTownBuilds()

        result = {}
        result['done'] = True
        result['builds'] = townBuildsService.get(
            townDomain,
            transfer.getUser()
        )

        result['queue'] = townBuildsService.getQueue(
            townDomain,
            transfer.getUser()
        )

        return result

    def getTownBuilds(self, transfer, data):
        townDomain = self._getParamsTown().getById(data['town'])

        transfer.send(
            '/town_builds/get_builds',
            self._getBuildsAndQueueData(transfer, townDomain)
        )

    def createBuild(self, transfer, data):
        townDomain = self._getParamsTown().getById(data['town'])

        self._getParamsAclTownBuilds().create(
            transfer.getUser(),
            data['town'],
            data['key'],
            data['level']
        )

        transfer.send(
            '/town_builds/create',
            self._getBuildsAndQueueData(transfer, townDomain)
        )

    def removeBuild(self, transfer, data):
        townDomain = self._getParamsTown().getById(data['town'])

        self._getParamsAclTownBuilds().remove(
            transfer.getUser(),
            data['town'],
            data['key'],
            data['level']
        )

        transfer.send(
            '/town_builds/remove',
            self._getBuildsAndQueueData(transfer, townDomain)
        )
