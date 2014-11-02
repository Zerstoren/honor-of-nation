import time

import service.TownBuilds
import service.Town

class CeleryPrivateController():
    def _getTownBuilds(self):
        return service.TownBuilds.Service_TownBuilds().decorate('Params')

    def _getParamsTown(self):
        return service.Town.Service_Town().decorate('Params')

    def buildComplete(self, message):
        if not (message['start_at'] + message['complete_after']) <= int(time.time()):
            raise Exception('Слишком рано')

        townDomain = self._getParamsTown().getById(message['town'])
        self._getTownBuilds().completeBuild(townDomain)
