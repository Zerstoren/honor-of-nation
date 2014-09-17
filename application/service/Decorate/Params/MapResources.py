import helpers.mongo

import service.User
import models.Map.Math


class Decorate():
    def getResourceByPosition(self, x, y):
        return super().getResourceByPosition(int(x), int(y))

    def saveResources(self, data):
        data['amount'] = int(data['amount'])
        data['base_output'] = int(data['base_output'])
        data['posId'] = models.Map.Math.fromStringCoordinateToPositionId(data['position'])

        if '_id' in data:
            data['_id'] = helpers.mongo.objectId(data['_id'])

        if 'user' in data and data['user']:
            if data['user'] == 'none':
                data['user'] = None
            else:
                data['user'] = service.User.Service_User().getUserDomain(
                    helpers.mongo.objectId(data['user'])
                ).getId()

        else:
            data['user'] = None

        if 'town' in data and data['town']:
            if data['town'] == 'none':
                data['town'] = None
            else:
                data['town'] = None # TODO
        else:
            data['town'] = None

        return super().saveResources(data)