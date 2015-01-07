from .Abstract import AbstractService

import init_celery

import service.Army
import models.Equipment.Units.Common as Units_Common

from models.ArmyQueue.Domain import ArmyQueue_Domain
from models.ArmyQueue.Factory import ArmyQueue_Factory

import config
import time


class Service_ArmyQueue(AbstractService.Service_Abstract):
    def add(self, town, unit, count, user=None):
        resourcesDomain = town.getUser().getResources()
        armyQueueDomain = ArmyQueue_Domain()

        if count != 1 and unit.getType() == Units_Common.TYPE_GENERAL:
            count = 1
        elif count >= int(config.get('rules.soliders_create_max_size')):
            count = int(config.get('rules.soliders_create_max_size'))

        price = {
            'rubins': count *  unit.getRubins(),
            'wood': count * unit.getWood(),
            'steel': count * unit.getSteel(),
            'eat': count * unit.getEat(),
            'stone': 0,
            'time': count * unit.getTime()
        }

        armyQueueDomain.setUnit(unit)
        armyQueueDomain.setTown(town)
        armyQueueDomain.setCount(count)
        armyQueueDomain.setCompleteAfter(price['time'])
        armyQueueDomain.setStartAt(None)
        armyQueueDomain.setQueueCode(None)

        resourcesDomain.dropResources(price)
        resourcesDomain.getMapper().save(resourcesDomain)
        armyQueueDomain.getMapper().save(armyQueueDomain)

        self._updateQueueCode(town)

    def remove(self, town, queueDomain, user=None):
        resourcesDomain = town.getUser().getResources()

        unitDomain = queueDomain.getUnit()
        countDiscard = queueDomain.getCount()

        if queueDomain.getQueueCode():
            init_celery.app.control.revoke(queueDomain.getQueueCode())

            startAt = queueDomain.getStartAt()
            completeAfter = queueDomain.getCompleteAfter()

            percentComplete = ((startAt + completeAfter) - int(time.time())) / completeAfter
            countComplete = int(percentComplete * queueDomain.getCount())
            countDiscard = queueDomain.getCount() - countComplete

            armyService = service.Army.Service_Army()
            armyService.create(
                unitDomain,
                town,
                countComplete
            )

        price = {
            'rubins': countDiscard *  unitDomain.getRubins(),
            'wood': countDiscard * unitDomain.getWood(),
            'steel': countDiscard * unitDomain.getSteel(),
            'eat': countDiscard * unitDomain.getEat(),
            'stone': 0
        }
        resourcesDomain.upResources(price)

        queueDomain.getMapper().remove(queueDomain)
        self._updateQueueCode(town)

    def getQueue(self, town, user=None):
        return self._getQueue(town)

    def create(self, queueId):
        queueDomain = ArmyQueue_Factory.get(queueId)

        armyService = service.Army.Service_Army()
        armyService.create(
            queueDomain.getUnit(),
            queueDomain.getTown(),
            queueDomain.getCount()
        )

        # Complete
        queueDomain.getMapper().remove(queueDomain)
        self._updateQueueCode(queueDomain.getTown())

        return queueDomain.getTown()

    def _getQueue(self, town):
        return ArmyQueue_Factory.load(town)

    def _updateQueueCode(self, town):
        queue = self._getQueue(town)
        if len(queue) == 0 or queue[0].getQueueCode():
            return False

        currentQueue = queue[0]

        queueItem = {
            'queue_id': str(currentQueue.getId()),
            'complete_after': currentQueue.getCompleteAfter(),
            'start_at': int(time.time())
        }

        currentQueue.setStartAt(int(time.time()))
        currentQueue.setQueueCode(
            str(init_celery.army.apply_async((queueItem, ), countdown=queueItem['complete_after']))
        )

        currentQueue.getMapper().save(currentQueue)

        return True

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_ArmyQueue
        """
        return super().decorate(*args)
