from models.Equipment.Armor import Common

import helpers.mongo

from models.User.Factory import User_Factory


class Decorate(object):
    def _fixParams(self, data):
        assert(data['type'] in [Common.TYPE_ARMOR_LEATHER, Common.TYPE_ARMOR_MAIL, Common.TYPE_ARMOR_PLATE])

        if data['shield']:
            assert(data['shield_type'] in [Common.TYPE_SHIELD_WOOD, Common.TYPE_SHIELD_STEEL])

        if 'user' in data:
            data['user'] = helpers.mongo.objectId(data['user'])

        data['health'] = int(data['health'])
        data['agility'] = int(data['agility'])
        data['absorption'] = int(data['absorption'])

        data['shield'] = bool(data['shield'])
        data['shield_type'] = data['shield_type']
        data['shield_blocking'] = int(data['shield_blocking'])
        data['shield_durability'] = int(data['shield_durability'])

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