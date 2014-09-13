from .Abstract import AbstractService

import models.MapResources.Factory
import models.MapResources.Mapper
import models.MapResources.Domain

import models.Map.Math

import service.User

import helpers.mongo

import exceptions.database
import exceptions.message

class Service_MapResources(AbstractService.Service_Abstract):

    def getResourceByPosition(self, x, y):
        resource = models.MapResources.Mapper.MapResources_Mapper.getResourceByPosition(x, y)

        if resource is False:
            return False

        return models.MapResources.Factory.MapResources_Factory.getDomainFromData(resource)

    def saveResources(self, data):
        posId = models.Map.Math.fromStringCoordinateToPositionId(data['domain']['position'])

        try:
            domainInPosition = models.MapResources.Factory.MapResources_Factory.getDomainByPosition(
                *models.Map.Math.fromIdToPosition(posId)
            )

            if '_id' not in data['domain']:
                raise exceptions.message.Message('Данная позиция уже занята')
            elif '_id' in data['domain'] and str(domainInPosition.getId()) != data['domain']['_id']:
                raise exceptions.message.Message('Данная позиция уже занята')

        except exceptions.database.NotFound:
            pass

        if '_id' in data['domain']:
            domain = models.MapResources.Factory.MapResources_Factory.getDomainById(data['domain']['_id'])
        else:
            domain = models.MapResources.Domain.MapResources_Domain()

        if data['domain']['user']:
            user = service.User.Service_User().getUserDomain(
                helpers.mongo.objectId(data['domain']['user'])
            ).getId()
        else:
            user = None

        if data['domain']['town']:
            town = None # TODO
        else:
            town = None


        domain.setOptions({
            'amount': int(data['domain']['amount']),
            'base_output': int(data['domain']['base_output']),
            'output': self.calculateOutput(int(data['domain']['base_output'])),
            'pos_id': posId,
            'town':  town,
            'user': user,
            'type': data['domain']['type']
        })

        domain.getMapper().save(domain)

        return True

    def calculateOutput(self, baseOutput):
        return baseOutput

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_MapResources
        """
        return super().decorate(*args)
