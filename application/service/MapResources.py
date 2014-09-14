from .Abstract import AbstractService

import models.MapResources.Factory
import models.MapResources.Mapper
import models.MapResources.Domain

import models.Map.Math

import exceptions.database
import exceptions.message

class Service_MapResources(AbstractService.Service_Abstract):

    def getResourceByPosition(self, x, y):
        resource = models.MapResources.Mapper.MapResources_Mapper.getResourceByPosition(x, y)

        if resource is False:
            return False

        return models.MapResources.Factory.MapResources_Factory.getDomainFromData(resource)

    def saveResources(self, data):
        try:
            domainInPosition = models.MapResources.Factory.MapResources_Factory.getDomainByPosition(
                *models.Map.Math.fromIdToPosition(data['posId'])
            )

            if '_id' not in data:
                raise exceptions.message.Message('Данная позиция уже занята')
            elif '_id' in data and domainInPosition.getId() != data['_id']:
                raise exceptions.message.Message('Данная позиция уже занята')

        except exceptions.database.NotFound:
            pass

        if '_id' in data:
            domain = models.MapResources.Factory.MapResources_Factory.getDomainById(data['_id'])
        else:
            domain = models.MapResources.Domain.MapResources_Domain()

        domain.setOptions({
            'amount': int(data['amount']),
            'base_output': int(data['base_output']),
            'output': self._calculateOutput(int(data['base_output'])),
            'pos_id': data['posId'],
            'town': data['town'],
            'user': data['user'],
            'type': data['type']
        })

        domain.getMapper().save(domain)

        return True

    def _calculateOutput(self, baseOutput):
        return baseOutput

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_MapResources
        """
        return super().decorate(*args)
