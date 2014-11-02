import exceptions.builds

import models.Abstract.Domain
import models.Town.Factory
import models.Town.Domain

from .Mapper import TownBuilds_Mapper

import time


class TownBuilds_Domain(models.Abstract.Domain.Abstract_Domain):
    def getTown(self):
        return models.Town.Factory.Town_Factory.getDomainById(
            self._domain_data['town']
        )

    def setTown(self, town):
        if isinstance(town, models.Town.Domain.Town_Domain):
            self._domain_data['town'] = town.getId()
        else:
            self._domain_data['town'] = town

    def addToQueue(self, key, level, completeAfter):
        buildLevel = self.getMaximumBuildLevel(key)

        if not buildLevel + 1 == level:
            raise exceptions.builds.WrongCreateBuildLevel('Current level build %s is %s, you try create level %s' % (
                key, buildLevel, level
            ))

        queue = self.getQueue()
        queue.append({
            'key': key,
            'level': level,
            'complete_after': completeAfter,
            'start_at': None,
            'queue_code': None
        })

        self.setQueue(queue)

    def removeFromQueue(self, key, level):
        queue = self.getQueue()
        queueCode = None
        items = []

        for i in list(queue):
            if i['key'] == key and i['level'] >= level:
                if i['queue_code']:
                    queueCode = i['queue_code']

                items.append(i)
                queue.remove(i)

        self.setQueue(queue)

        return (queueCode, items, )

    def setQueueCode(self, queueCode):
        queue = self.getQueue()

        if len(queue) and queue[0]['queue_code'] != None:
            raise exceptions.builds.WrongQueueChain('First build in queue is under construction')

        queue[0]['queue_code'] = str(queueCode)
        queue[0]['start_at'] = int(time.time())

        self.setQueue(queue)

    def hasQueueCode(self):
        queue = self.getQueue()
        return bool(len(queue)) and queue[0]['queue_code'] != None

    def getMaximumBuildLevel(self, key):
        queue = self.getQueue()

        maxLevel = self._getFunc(key)()

        for i in queue:
            if i['key'] == key:
                maxLevel = i['level']

        return maxLevel

    def getMapper(self):
        """
        required method, for IDE static analyzer
        """
        return TownBuilds_Mapper
