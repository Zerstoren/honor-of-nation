import exceptions.httpCodes

import models.Equipment.Armor.Factory

class Decorate(object):
    def _canAccess(self, domain, user):
        if domain.getUser().getId() != user.getId():
            raise exceptions.httpCodes.Page403("Cant access to weapon")

    def get(self, _id, user=None):
        domain = super().get(_id, user)
        self._canAccess(domain, user)

        return domain

    def remove(self, _id, user=None):
        domain = models.Equipment.Armor.Factory.Equipment_Armor_Factory.get(_id)
        self._canAccess(domain, user)

        return super().remove(_id, user)
