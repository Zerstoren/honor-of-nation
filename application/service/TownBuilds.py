import service.Abstract.AbstractService

import models.TownBuilds.Factory
import models.TownBuilds.Math

import time
import copy

import init_celery


class Service_TownBuilds(service.Abstract.AbstractService.Service_Abstract):
    def get(self, townDomain, user=None):
        return townDomain.getBuilds()

    def getQueue(self, townDomain, user=None):
        return townDomain.getBuilds().getQueue()

    def completeBuild(self, townDomain):
        buildsDomain = townDomain.getBuilds()
        buildsInQueue = buildsDomain.getQueue()
        buildInQueue = buildsDomain.getQueue()[0]

        buildsInQueue.remove(buildInQueue)
        self._updateQueueCode(buildsDomain)

        buildsDomain.set(buildInQueue['key'], buildInQueue['level'])
        buildsDomain.getMapper().save(buildsDomain)

    def create(self, user, townDomain, buildKey, level):
        buildsDomain = townDomain.getBuilds()

        if level >= buildsDomain.getMaximalLevel(buildKey):
            level = buildsDomain.getMaximalLevel(buildKey)

        resourceDomain = townDomain.getUser().getResources()

        maxBuildLevel = buildsDomain.getMaximumBuildLevel(buildKey)

        for i in range(maxBuildLevel + 1, level + 1):
            price = models.TownBuilds.Math.getBuildPrice(buildKey, i)
            resourceDomain.dropResources(price)

            buildsDomain.addToQueue(
                buildKey,
                i,
                price['time']
            )

        self._updateQueueCode(buildsDomain)

        resourceDomain.getMapper().save(resourceDomain)
        buildsDomain.getMapper().saveQueue(buildsDomain)

    def remove(self, user, townDomain, buildKey, level):

        buildsDomain = townDomain.getBuilds()
        resourceDomain = townDomain.getUser().getResources()

        queueCode, buildsToRemove = buildsDomain.removeFromQueue(buildKey, level)

        if queueCode:
            init_celery.app.control.revoke(queueCode)
            self._updateQueueCode(buildsDomain)

        for build in buildsToRemove:
            percentComplete = 1
            if 'queue_code' in build and build['queue_code']:
                percentComplete = (
                    (
                        (
                            build['start_at'] + build['complete_after']
                        ) - int(time.time())
                    ) /  build['complete_after']
                )

            price = models.TownBuilds.Math.getBuildPrice(build['key'], build['level'], percentComplete)
            resourceDomain.upResources(price)

        resourceDomain.getMapper().save(resourceDomain)
        buildsDomain.getMapper().save(buildsDomain)

    def _updateQueueCode(self, buildsDomain):
        if not buildsDomain.hasQueueCode() and len(buildsDomain.getQueue()):
            queue = copy.copy(buildsDomain.getQueue()[0])
            queue['town'] = str(buildsDomain.getTown().getId())
            queue['start_at'] = int(time.time())
            queueCode = init_celery.builds.apply_async((queue, ), countdown=queue['complete_after'])

            buildsDomain.setQueueCode(queueCode)

            return True

        return False

    def decorate(self, *args):
        """
        :rtype: Service_TownBuilds
        """
        return super().decorate(*args)
