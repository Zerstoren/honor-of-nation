import time

import system.log

from service.ArmyQueue import Service_ArmyQueue
from service.Army import Service_Army

from service.Town import Service_Town


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
        return Service_ArmyQueue().decorate(Service_ArmyQueue.PARAMS_JSONPACK_ACL)

    def _getParamsTownService(self):
        return Service_Town().decorate(Service_Town.PARAMS)


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

        DeliveryController().armyChange(
            self._getParamsTownService().getById(data['town'])
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

        self._getParamsArmyQueueService().create(message['queue_id'])

        DeliveryController().armyChange(
            self._getParamsTownService().getById(message['town'])
        )


class DeliveryController(_AbstractArmyQueue):
    def armyChange(self, town):
        """
        :type town: models.Town.Domain.Town_Domain
        """
        town.getUser().getTransfer().forceSend('/delivery/unitsUpdate',
            {
                'done': True,
                'town': str(town.getId()),
                'armyQueue': self._getJsonPackArmyQueueService().getQueue(town)
            }
        )