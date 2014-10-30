import service.Abstract.AbstractService

import models.TownBuilds.Factory
import models.TownBuilds.Math

import time

import init_celery


class Service_TownBuilds(service.Abstract.AbstractService.Service_Abstract):
    def get(self, townDomain, user):
        return models.TownBuilds.Factory.TownBuilds_Factory.getByTown(townDomain)

    def completeBuild(self, townDomain):
        buildsDomain = townDomain.getBuilds()
        buildInQueue = buildsDomain.getQueue()[0]

        buildsDomain.removeFromQueue(buildInQueue['key'], buildInQueue['level'])
        self._updateQueueCode(buildsDomain)

        buildsDomain.getMapper().save(buildsDomain)

    def create(self, townDomain, buildKey, level):
        buildsDomain = townDomain.getBuilds()
        resourceDomain = townDomain.getUser().getResources()

        maxBuildLevel = buildsDomain.getMaximumBuildLevel(buildKey)

        for i in range(maxBuildLevel, level):
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

    def remove(self, townDomain, buildKey, level):
        buildsDomain = townDomain.getBuilds()
        resourceDomain = townDomain.getUser().getResources()
        queueCode, buildsToRemove = buildsDomain.removeFromQueue(buildKey, level)

        if queueCode:
            init_celery.app.control.revoke(queueCode)
            self._updateQueueCode(buildsDomain)

        for build in buildsToRemove:
            percentComplete = 1
            if 'queue_code' in build:
                percentComplete = ((build['start_at'] + build['complete_after']) - time.time()) /  build['complete_after']

            price = models.TownBuilds.Math.getBuildPrice(build['key'], build['level'], percentComplete)
            resourceDomain.upResources(price)

        resourceDomain.getMapper().save(resourceDomain)
        buildsDomain.getMapper().save(buildsDomain)

    def _updateQueueCode(self, buildsDomain):
        if not buildsDomain.hasQueueCode() and len(buildsDomain.getQueue()):
            queue = buildsDomain.getQueue()[0]
            queueCode = init_celery.builds.apply_async(queue, countdown=queue['time'])
            buildsDomain.setQueueCode(queueCode)

            return True

        return False

    def decorate(self, *args):
        """
        :rtype: Service_TownBuilds
        """
        return super().decorate(*args)
