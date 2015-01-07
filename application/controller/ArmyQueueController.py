import time

import system.log

from service.ArmyQueue import Service_ArmyQueue
from service.Army import Service_Army


class _AbstractArmyQueue(object):
    def _getParamsArmyService(self):
        return Service_Army().decorate(Service_Army.PARAMS)

    def _getParamsArmyQueueService(self):
        return Service_ArmyQueue().decorate(Service_ArmyQueue.PARAMS)

    def _getJsonPackArmyQueueService(self):
        return Service_ArmyQueue().decorate(Service_ArmyQueue.JSONPACK)

    def _getParamsAclArmyQueueService(self):
        return Service_ArmyQueue().decorate(Service_ArmyQueue.PARAMS_ACL)

    def _getParamsAclJsonPackArmyQueueService(self):
        return Service_ArmyQueue().decorate(Service_ArmyQueue.PARAMS_ACL_JSONPACK)


class MainController(_AbstractArmyQueue):
    def create(self, transfer, data):
        self._getParamsAclArmyQueueService().add(
            data['town'],
            data['unit'],
            data['count'],
            transfer.getUser()
        )

        transfer.send('/army/queue/add', {
            'done': True
        })

    def remove(self, transfer, data):
        self._getParamsAclArmyQueueService().remove(
            data['town'],
            data['queue_id'],
            transfer.getUser()
        )

        transfer.send('/army/queue/remove', {
            'done': True
        })


class CollectionController(_AbstractArmyQueue):
    def load(self, transfer, data):
        result = self._getParamsAclJsonPackArmyQueueService().getQueue(
            data['town'],
            transfer.getUser()
        )

        transfer.send('/collection/army/queue/load', {
            'done': True,
            'data': result
        })


class CeleryPrivateController(_AbstractArmyQueue):
    def armyCreated(self, message):
        if not (message['start_at'] + message['complete_after']) <= int(time.time()):
            system.log.critical('To early. %s. Current time %i' % (str(message), int(time.time())))
            raise Exception('Слишком рано')

        town = self._getParamsArmyQueueService().create(message['queue_id'])
        town.getUser().getTransfer().forceSend('/delivery/unitsUpdate',
            {
                'done': True,
                'town': str(town.getId()),
                'armyQueue': self._getJsonPackArmyQueueService().getQueue(town)
            }
        )
