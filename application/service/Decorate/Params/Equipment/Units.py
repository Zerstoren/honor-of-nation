from models.Equipment.Units import Common

import helpers.mongo

from models.User.Factory import User_Factory


class Decorate(object):
    def _fixParams(self, data):
        assert(data['type'] in [Common.TYPE_SOLIDER, Common.TYPE_GENERAL])

        if 'user' in data:
            data['user'] = helpers.mongo.objectId(data['user'])

        data['troop_size'] = int(data['troop_size'])
        data['health'] = int(data['health'])
        data['agility'] = int(data['agility'])
        data['absorption'] = int(data['absorption'])
        data['stamina'] = int(data['stamina'])
        data['strength'] = int(data['strength'])

        data['armor'] = helpers.mongo.objectId(data['armor'])
        data['weapon'] = helpers.mongo.objectId(data['weapon'])

        if data['weapon_second']:
            data['weapon_second'] = helpers.mongo.objectId(data['weapon_second'])
        else:
            data['weapon_second'] = False

        return data

    def save(self, data, user=None):
        data = self._fixParams(data)
        return super().save(data, user)

    def simulate(self, data):
        data = self._fixParams(data)
        return super().simulate(data)

    def get(self, _id, user=None):
        _id = helpers.mongo.objectId(_id)
        return super().get(_id, user)

    def load(self, user):
        userId = helpers.mongo.objectId(user)
        user = User_Factory.getDomainById(userId)
        return super().load(user)

    def remove(self, _id, user=None):
        return super().remove(
            helpers.mongo.objectId(_id),
            user
        )