from models.Equipment.Weapon import Common

import helpers.mongo

from models.User.Factory import User_Factory


class Decorate(object):
    def _fixParams(self, data):
        assert(data['type'] in [Common.TYPE_BOW, Common.TYPE_SPEAR, Common.TYPE_BLUNT, Common.TYPE_SWORD])

        if 'user' in data:
            data['user'] = helpers.mongo.objectId(data['user'])

        data['damage'] = int(data['damage'])
        data['speed'] = int(data['speed'])
        data['critical_chance'] = int(data['critical_chance'])
        data['critical_damage'] = float(data['critical_damage'])

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