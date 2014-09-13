from .Abstract import AbstractService

import models.MapResources.Factory
import models.MapResources.Mapper
import models.MapResources.Domain

import models.Map.Math

import service.User

import helpers.mongo

class Service_MapResources(AbstractService.Service_Abstract):

    def getResourceByPosition(self, x, y):
        resource = models.MapResources.Mapper.MapResources_Mapper.getResourceByPosition(x, y)

        if resource is False:
            return False

        return models.MapResources.Factory.MapResources_Factory.getDomainFromData(resource)

    def saveResources(self, data):
        if '_id' in data:
            domain = models.MapResources.Factory.MapResources_Factory.getDomainById(data['_id'])
        else:
            domain = models.MapResources.Domain.MapResources_Domain()

        user = service.User.Service_User().getUserDomain(
            helpers.mongo.objectId(data['user'])
        )

        domain.setOptions({
            'amount': int(data['amount']),
            'base_output': int(data['base_output']),
            'output': int(data['output']),
            'pos_id': models.Map.Math.fromStringCoordinateToPositionId(data['position']),
            'town':  None, # TODO
            'user': user
        })

        domain.getMapper().save(domain)


    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_MapResources
        """
        return super().decorate(*args)
