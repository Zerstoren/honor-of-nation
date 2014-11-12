import service.TownBuilds
import service.Town

import time


class AbstractTownBuildsController(object):
    def _getParamsTown(self):
        return service.Town.Service_Town().decorate('Params')

    def _getAclJsonPackTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Acl', 'JsonPack')

    def _getParamsAclTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Params', 'Acl')

    def _getJsonPackTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('JsonPack')

    def _getParamsTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Params')


class MainController(AbstractTownBuildsController):
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


class CeleryPrivateController(AbstractTownBuildsController):
    def buildComplete(self, message):
        if not (message['start_at'] + message['complete_after']) <= int(time.time()):
            raise Exception('Слишком рано')

        townDomain = self._getParamsTown().getById(message['town'])
        self._getParamsTownBuilds().completeBuild(townDomain)

        service = self._getJsonPackTownBuilds()
        builds = service.get(townDomain)
        queue = service.getQueue(townDomain)

        user = townDomain.getUser()
        user.getTransfer().send('/delivery/buildsUpdate', {
            'done': True,
            'town': str(townDomain.getId()),
            'builds': builds,
            'queue': queue
        }, True)
